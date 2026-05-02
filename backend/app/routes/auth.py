from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.schemas.auth import RegisterRequest, TokenResponse
from app.services.auth_services import hash_password, verify_password, create_token
from app.models.user import user_model
from app.database import users_collection

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    existing_user = await users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed = hash_password(data.password)
    user = user_model(data.name, data.email, hashed)
    await users_collection.insert_one(user)
    return {"message": "Account created successfully! ✅"}

# ─── Login ────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login(data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm mein username field hota hai email ke liye
    user = await users_collection.find_one({"email": data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    token = create_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })
    return {"access_token": token, "token_type": "bearer"}