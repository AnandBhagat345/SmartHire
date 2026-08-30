from fastapi import APIRouter, HTTPException,Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from app.schemas.auth import RegisterRequest, TokenResponse
from app.services.auth_services import (
    hash_password,
    verify_password,
    create_token
)

from app.models.user import user_model
from app.database import users_collection
from app.services.rate_limiter import RateLimiter



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

rate_limiter = RateLimiter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request, data: RegisterRequest):
    
    # Redis Sliding Window Rate Limiting (IP-based)
    client_ip = request.client.host

    cache_key = f"rate_limit:register:ip:{client_ip}"

    allowed, request_count = await rate_limiter.is_allowed(
        key=cache_key,
        limit=5,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many registration attempts. Please try again later."
        )

    existing_user = await users_collection.find_one(
        {"email": data.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed = hash_password(data.password)

    user = user_model(
        data.name,
        data.email,
        hashed
    )

    await users_collection.insert_one(user)

    return {
        "message": "Account created successfully! ✅"
    }


# ---- Login ---
@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    data: OAuth2PasswordRequestForm = Depends()
):
    client_ip = request.client.host

    ip_cache_key = f"rate_limit:login:ip:{client_ip}"

    allowed, request_count = await rate_limiter.is_allowed(
        key=ip_cache_key,
        limit=10,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts from this IP. Please try again later."
        )
        
    
    email_cache_key = f"rate_limit:login:email:{data.username}"

    allowed, request_count = await rate_limiter.is_allowed(
        key=email_cache_key,
        limit=5,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts for this account. Please try again later."
        )

    # OAuth2 username field = email
    user = await users_collection.find_one(
        {"email": data.username}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(
        data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }