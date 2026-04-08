from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "academic_writing_copilot",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_always_eager=settings.celery_task_always_eager,
    task_eager_propagates=True,
)

celery_app.autodiscover_tasks(["app.workers"])
