from pydantic import BaseModel
from typing import List

class AnalysisResponse(BaseModel):
    ats_score: int
    missing_keywords: List[str]
    ats_feedback: str
    recruiter_feedback: str
    suggestions: List[str]