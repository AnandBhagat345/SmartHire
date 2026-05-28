from pydantic import BaseModel, EmailStr, Field

# Register ke liye input shape
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr        # Automatically email validate karta hai
    password: str = Field(min_length=6, max_length=64)

# Login ke liye input shape
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Token response shape
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"