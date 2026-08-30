from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, resume, jobs


from contextlib import asynccontextmanager
from app.redis import redis_client



@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        await redis_client.ping()
        print("Redis connected successfully")

    except Exception as e:
        print(f"Redis connection failed: {e}")

    yield

    await redis_client.aclose()
    print("Redis connection closed")

app = FastAPI(
    title="SmartHire API",
    description="AI-powered Resume Analyzer",
    version="1.0.0",
    lifespan=lifespan
)

app.state.testing = False

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "http://localhost:5173",
        "https://smart-hire-pied-eta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "SmartHire API is running 🚀"}