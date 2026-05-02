
from dotenv import load_dotenv
# .env file load karo
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import users_collection
from app.routes.auth import router
from app.routes import resume

from app.middleware.auth_middleware import get_current_user
from fastapi import Depends






# FastAPI app banao
app = FastAPI(
    title="SmartHire API",
    description="AI-powered Resume Analyzer",
    version="1.0.0"
)

# CORS — Frontend ko Backend se baat karne deta hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Test route
@app.get("/")
def root():
    return {"message": "SmartHire API is running 🚀"}

@app.get("/test-db")
async def test_db():
    await users_collection.insert_one({"status": "connected"})
    return {"message": "DB Connected Successfully 🚀"}

@app.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return {"user": current_user}