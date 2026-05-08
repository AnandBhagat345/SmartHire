from datetime import datetime
from typing import Optional

def job_model(
    user_id: str,
    company_name: str,
    job_role: str,
    status: str,
    job_link: Optional[str] = None,      # optional
    application_date: Optional[str] = None,  # optional
    notes: Optional[str] = None,         # optional
    follow_up_date: Optional[str] = None # optional
):
    return {
        "user_id": user_id,
        "company_name": company_name,
        "job_role": job_role,
        "job_link": job_link,
        "status": status,
        "application_date": application_date,
        "notes": notes,
        "follow_up_date": follow_up_date,
        "created_at": datetime.utcnow()
    }