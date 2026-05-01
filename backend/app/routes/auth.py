from fastapi import APIRouter, HTTPException, status
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from services.auth_services import hash_password, verify_password, create_token
from models.user import user_model
from app.database import users_collection

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ─── Register ────────────

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    # Checking email already exist or not
    existing_user = await users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Password hash 
    hashed = hash_password(data.password)
    
    # User model 
    user = user_model(data.name, data.email, hashed)
    
    # saved in MongoDB  
    await users_collection.insert_one(user)
    
    return {"message": "Account created successfully! ✅"}

# ─── Login ─────────────

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    # find User 
    user = await users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Password verify 
    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Token banao
    token = create_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })
    
    return {"access_token": token, "token_type": "bearer"}