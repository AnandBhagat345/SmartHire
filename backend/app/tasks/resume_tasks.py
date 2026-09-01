from app.celery_app import celery_app
from app.services.ai_services import analyze_resume
from app.database_sync import resumes_collection_sync
from app.models.resume import resume_model


@celery_app.task
def analyze_resume_task(
    resume_text: str,
    job_description: str,
    user_id: str
):
    print("Resume analysis task started")

    # AI Analysis
    result = analyze_resume(
        resume_text,
        job_description
    )

    # AI Error check
    if "error" in result:
        return {
            "error": result["error"]
        }

    # Create MongoDB document
    document = resume_model(
        user_id=user_id,
        job_description=job_description,
        ats_score=result["ats_score"],
        missing_keywords=result["missing_keywords"],
        ats_feedback=result["ats_feedback"],
        recruiter_feedback=result["recruiter_feedback"],
        suggestions=result["suggestions"]
    )

    # Save permanently in MongoDB
    resumes_collection_sync.insert_one(document)

    print("Resume analysis task completed")

    # Return result to Celery Result Backend
    return {
        **result,
        "resume_text": resume_text
    }