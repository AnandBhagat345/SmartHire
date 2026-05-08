from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_user
from app.database import jobs_collection
from app.models.job import job_model
from app.schemas.job import JobCreate, JobUpdate
from bson import ObjectId

router = APIRouter(prefix="/jobs", tags=["Job Tracker"])

#  Create Job
@router.post("/")
async def create_job(data: JobCreate, current_user = Depends(get_current_user)):
    
    # job_model banao
    document = job_model(
        user_id=current_user["user_id"],
        company_name=data.company_name,
        job_role=data.job_role,
        status=data.status,
        job_link=data.job_link,
        application_date=data.application_date,
        notes=data.notes,
        follow_up_date=data.follow_up_date
    )
    
    # Save in Mongodb
    result = await jobs_collection.insert_one(document)
    
    return {"message": "Job added ✅", "id": str(result.inserted_id)}

#  Get All Jobs
@router.get("/")
async def get_jobs(current_user = Depends(get_current_user)):

    # Newest pehle
    cursor = jobs_collection.find(
        {"user_id": current_user["user_id"]}
    ).sort("created_at", -1)
    
    jobs = await cursor.to_list(length=100)
    
    # convert _id
    for job in jobs:
        job["_id"] = str(job["_id"])
    
    return jobs
    

# Update Job
@router.put("/{job_id}")
async def update_job(job_id: str, data: JobUpdate, current_user = Depends(get_current_user)):
    
    # only given fields  update (None wale skip)
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    result = await jobs_collection.update_one(
        {"_id": ObjectId(job_id), "user_id": current_user["user_id"]},
        {"$set": update_data}
    )
    
    # if not job 
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"message": "Job updated ✅"}

# Delete Job
@router.delete("/{job_id}")
async def delete_job(job_id: str, current_user = Depends(get_current_user)):
    
    result = await jobs_collection.delete_one(
        {"_id": ObjectId(job_id), "user_id": current_user["user_id"]}
    )
    
    # If job not exist
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"message": "Job deleted ✅"}
    