from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, resume

app = FastAPI(
    title="SmartHire API",
    description="AI-powered Resume Analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)

@app.get("/")
def root():
    return {"message": "SmartHire API is running 🚀"}