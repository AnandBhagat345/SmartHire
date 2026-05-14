from pydantic import BaseModel, field_validator, model_validator
from typing import List, Literal

class AnalysisResponse(BaseModel):
    candidate_level: Literal["FRESHER", "JUNIOR", "MID-LEVEL", "SENIOR"]
    jd_required_level: Literal["FRESHER", "JUNIOR", "MID-LEVEL", "SENIOR"]
    level_mismatch: str
    ats_score: int
    missing_keywords: List[str]
    quality_issues: List[str]
    ats_feedback: str
    recruiter_feedback: str
    suggestions: List[str]

    # SCORE VALIDATOR 
    @field_validator("ats_score")
    def score_range(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Score must be between 0 and 100")
        return v

    #  SUGGESTIONS 
    @field_validator("suggestions")
    def min_suggestions(cls, v):
        if len(v) < 3:
            raise ValueError("At least 3 suggestions required")
        return v

    @field_validator("suggestions", mode="before")
    def no_blank_suggestions(cls, v):
        return [i.strip() for i in v if i.strip()]

    # QUALITY ISSUES 
    @field_validator("quality_issues")
    def min_quality_issues(cls, v):
        if len(v) < 1:
            raise ValueError("At least 1 quality issue required")
        return v

    #  MISSING KEYWORDS 
    @field_validator("missing_keywords", mode="before")
    def no_blank_keywords(cls, v):
        return [i.strip() for i in v if i.strip()]

    # LEVEL MISMATCH 
    @field_validator("level_mismatch")
    def normalize_level_mismatch(cls, v):
        if not v or v.strip() == "":
            return "none"
        return v

    # FEEDBACK LENGTH 
    @field_validator("ats_feedback", "recruiter_feedback")
    def min_feedback_length(cls, v):
        if len(v.split()) < 10:
            raise ValueError("Feedback too short")
        return v

    # CROSS FIELD VALIDATION 
    @model_validator(mode="after")
    def fresher_score_cap(self):
        if self.candidate_level == "FRESHER" and self.ats_score > 75:
            self.ats_score = 75
        return self
    
    # Rewrite for input
class RewriteRequest(BaseModel):
    resume_text: str
    job_description: str

# Rewrite for output
class RewriteResponse(BaseModel):
    rewritten_text: str