from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_resume(
    current_user = Depends(get_current_user)  
):
    
    print(current_user["user_id"])
    
    return {
        "message": "Resume upload route working 🚀",
        "user": current_user
    }
    