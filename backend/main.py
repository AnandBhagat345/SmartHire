from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import users_collection

# .env file load karo
load_dotenv()

# FastAPI app banao
app = FastAPI(
    title="SmartHire API",
    description="AI-powered Resume Analyzer",
    version="1.0.0"
)

# CORS — Frontend ko Backend se baat karne deta hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React ka default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def root():
    return {"message": "SmartHire API is running 🚀"}

@app.get("/test-db")
async def test_db():
    await users_collection.insert_one({"status": "connected"})
    return {"message": "DB Connected Successfully 🚀"}