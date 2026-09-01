
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, resume, jobs


from contextlib import asynccontextmanager
from app.redis import redis_client

from celery.result import AsyncResult
from app.celery_app import celery_app
from app.tasks.resume_tasks import analyze_resume_task


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
    

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):

    task_result = AsyncResult(
        task_id,
        app=celery_app
    )

    response = {
        "task_id": task_id,
        "status": task_result.status
    }

    if task_result.successful():
        response["result"] = task_result.result

    return response


@app.post("/test-resume-task")
async def test_resume_task():

    resume_text = """
    I am a Python Backend Developer.
    Skills: Python, FastAPI, Django, MongoDB, Redis, Docker, SQL.
    I have built REST APIs and AI-based applications.
    """

    job_description = """
    We are looking for a Python Backend Developer.
    Required skills: Python, FastAPI, REST APIs, SQL, Docker, Redis.
    """

    task = analyze_resume_task.delay(
        resume_text,
        job_description,
        "test_user_123"
    )

    return {
        "message": "Resume analysis started in background",
        "task_id": task.id
    }