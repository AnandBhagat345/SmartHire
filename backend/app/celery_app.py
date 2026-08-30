from celery import Celery


celery_app = Celery(
    "smarthire",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/1"
)

celery_app.conf.update(
    task_track_started=True
)