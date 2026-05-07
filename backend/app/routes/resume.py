from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.middleware.auth_middleware import get_current_user
from app.services.pdf_services import extract_text_from_pdf
from app.services.ai_services import analyze_resume
from app.schemas.resume import AnalysisResponse
from fastapi import HTTPException

from app.database import resumes_collection
from app.models.resume import resume_model

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
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
    
    return result

@router.get("/history")
async def get_history(
    current_user = Depends(get_current_user)
    ):
    cursor = resumes_collection.find({"user_id":current_user["user_id"]})

    analyses = await cursor.to_list(length=100)
    
    for analysis in analyses:
        analysis["_id"] = str(analysis["_id"])
    
    return analyses
        
  