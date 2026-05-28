from pydantic import BaseModel
from typing import Optional,List, Literal
from datetime import datetime



# Create new application
class JobCreate(BaseModel):
    company_name: str
    job_role: str
    status: Literal[ "Saved",   "Applied",   "Interview", "OA Round", "HR Round"  "Rejected",   "Offer"]

    
    job_link: Optional[str] = None
    application_date: Optional[str] = None
    
    notes: Optional[str] = None
    follow_up_date: Optional[str] = None


# Update existing application
class JobUpdate(BaseModel):
    status: Optional[str] = None
    
    notes: Optional[str] = None
    follow_up_date: Optional[str] = None


# Response sent to frontend
class JobResponse(BaseModel):
    id: str
    company_name: str
    job_role: str
    status: Literal[ "Saved",   "Applied",   "Interview",   "Rejected",   "Offer"]
    
    job_link: Optional[str] = None
    application_date: Optional[str] = None
    
    notes: Optional[str] = None
    follow_up_date: Optional[str] = None
    created_at: datetime