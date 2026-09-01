from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

celery_app = Celery(
    "smarthire",
    broker=f"{REDIS_URL}/1",
    backend=f"{REDIS_URL}/1",
    include=
        "app.tasks.resume_tasks"
)

celery_app.conf.update(
    task_track_started=True
)