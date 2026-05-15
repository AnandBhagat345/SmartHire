from datetime import datetime,UTC

def resume_model(
    user_id: str,
    job_description: str,
    ats_score: int,
    missing_keywords: list,
    ats_feedback: str,
    recruiter_feedback: str,
    suggestions: list
):
    return {
        "user_id": user_id,
        "job_description": job_description,
        "ats_score": ats_score,
        "missing_keywords": missing_keywords,
        "ats_feedback": ats_feedback,
        "recruiter_feedback": recruiter_feedback,
        "suggestions": suggestions,
        "created_at": datetime.now(UTC)
    }