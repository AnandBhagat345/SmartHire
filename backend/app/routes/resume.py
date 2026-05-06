from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.middleware.auth_middleware import get_current_user
from app.services.pdf_services import extract_text_from_pdf
from app.services.ai_services import analyze_resume
from app.schemas.resume import AnalysisResponse

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user = Depends(get_current_user)
):
    # Step 1: PDF se text nikalo
    resume_text = extract_text_from_pdf(file.file)
    
    
    # Step 2: AI ko bhejo
    result = analyze_resume(resume_text, job_description)
    
    # Step 3: Result return karo
    return result