from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
import os

from app.schemas.auth import RegisterRequest, TokenResponse
from app.services.auth_services import (
    hash_password,
    verify_password,
    create_token
)

from app.models.user import user_model
from app.database import users_collection

from fastapi import APIRouter, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.utils.rate_limit import rate_limit_exempt


limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# limiter bypass during Testing
def rate_limit_exempt():
    return os.getenv("TESTING") == "true"


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit(
    "5/minute",
    exempt_when=rate_limit_exempt
)
async def register(request: Request, data: RegisterRequest):

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
@limiter.limit(
    "10/minute",
    exempt_when=rate_limit_exempt
)
async def login(
    request: Request,
    data: OAuth2PasswordRequestForm = Depends()
):

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