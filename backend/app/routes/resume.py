from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Request

from app.middleware.auth_middleware import get_current_user
from app.services.pdf_services import extract_text_from_pdf

from app.schemas.resume import (
    RewriteRequest,
    RewriteResponse,
    InterviewRequest,
    InterviewResponse
)

from app.services.ai_services import (
    rewrite_resume,
    generate_interview_questions
)

from app.database import resumes_collection
from app.services.rate_limiter import RateLimiter
from app.tasks.resume_tasks import analyze_resume_task


# Router
router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

rate_limiter = RateLimiter()

# Analyze Resume

@router.post("/analyze")
async def analyze(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user=Depends(get_current_user)
):
    # Redis Sliding Window Rate Limiting
    cache_key = f"rate_limit:analyze:user:{current_user['user_id']}"

    allowed, request_count = await rate_limiter.is_allowed(
        key=cache_key,
        limit=5,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many resume analysis requests. Please try again later."
        )

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file)

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="PDF empty or unreadable"
        )

    # Send AI analysis task to Celery Worker
    task = analyze_resume_task.delay(
        resume_text,
        job_description,
        current_user["user_id"]
    )

    # Return immediately
    return {
        "message": "Resume analysis started",
        "task_id": task.id
    }

# Resume History

@router.get("/history")
async def get_history(
    current_user=Depends(get_current_user)
):

    cursor = resumes_collection.find({
        "user_id": current_user["user_id"]
    }).sort("created_at", -1)

    analyses = await cursor.to_list(length=100)

    for analysis in analyses:
        analysis["_id"] = str(analysis["_id"])

    return analyses



# Resume Rewrite


@router.post(
    "/rewrite",
    response_model=RewriteResponse
)
async def rewrite(
    request: Request,
    data: RewriteRequest,
    current_user=Depends(get_current_user)
):
    # Redis Sliding Window Rate Limiting
    cache_key = f"rate_limit:rewrite:user:{current_user['user_id']}"

    allowed, request_count = await rate_limiter.is_allowed(
        key=cache_key,
        limit=5,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many resume rewrite requests. Please try again later."
        )

    resume_text = data.resume_text
    job_description = data.job_description

    # AI Rewrite
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

    return {
        "rewritten_text": rewritten_resume
    }



# Interview Questions


@router.post(
    "/interview-prep",
    response_model=InterviewResponse
)
async def interview_prep(
    request: Request,
    data: InterviewRequest,
    current_user=Depends(get_current_user)
):
        # Redis Sliding Window Rate Limiting
    cache_key = f"rate_limit:interview:user:{current_user['user_id']}"

    allowed, request_count = await rate_limiter.is_allowed(
        key=cache_key,
        limit=5,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many interview preparation requests. Please try again later."
        )

    resume_text = data.resume_text
    job_description = data.job_description

    # AI Interview Questions
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