from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.middleware.auth_middleware import get_current_user
from app.services.pdf_services import extract_text_from_pdf
from app.services.ai_services import analyze_resume
from app.schemas.resume import AnalysisResponse


from app.database import resumes_collection
from app.models.resume import resume_model

from app.schemas.resume import AnalysisResponse, RewriteRequest, RewriteResponse,  InterviewRequest, InterviewResponse
from app.services.ai_services import analyze_resume, rewrite_resume, generate_interview_questions

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("5/minute")
async def analyze(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user = Depends(get_current_user)
):
    
    #  extract text from pdf
    resume_text = extract_text_from_pdf(file)
    
    if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="PDF empty or unreadable"
            )
    
    
    #  Sent to AI
    result = analyze_resume(resume_text, job_description)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    

    document = resume_model(
        user_id=current_user["user_id"],
        job_description=job_description,
        ats_score=result["ats_score"],
        missing_keywords=result["missing_keywords"],
        ats_feedback=result["ats_feedback"],
        recruiter_feedback=result["recruiter_feedback"],
        suggestions=result["suggestions"]
    )

    await resumes_collection.insert_one(document)
    
    return {
    **result,
    "resume_text": resume_text
    }

@router.get("/history")
async def get_history(
    current_user = Depends(get_current_user)
    ):
    cursor = resumes_collection.find({"user_id":current_user["user_id"]}).sort("created_at", -1)

    analyses = await cursor.to_list(length=100)
    
    for analysis in analyses:
        analysis["_id"] = str(analysis["_id"])
    
    return analyses

@router.post("/rewrite", response_model=RewriteResponse)
@limiter.limit("5/minute")
async def rewrite(
    request: Request,
    data: RewriteRequest,
    current_user = Depends(get_current_user)
):
    # user input 
    resume_text = data.resume_text
    job_description = data.job_description

    # AI rewrite service call 
    rewritten_resume = rewrite_resume(
        resume_text,
        job_description
    )

     # Error check
    if rewritten_resume.startswith("Error:"):
        raise HTTPException(
            status_code=500,
            detail=rewritten_resume
        )

    # response return
    return {"rewritten_text": rewritten_resume}


@router.post("/interview-prep", response_model=InterviewResponse)
@limiter.limit("5/minute")
async def interview_prep(
    request: Request,
    data: InterviewRequest,
    current_user = Depends(get_current_user)
):
    resume_text = data.resume_text
    job_description = data.job_description
    
    questions = generate_interview_questions(
        resume_text,
        job_description
    )
    
    # Error check
    if "error" in questions:
        raise HTTPException(
            status_code=500,
            detail=questions["error"]
        )

    return questions


        
  