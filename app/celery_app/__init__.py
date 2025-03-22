from celery import Celery
from celery.schedules import crontab

import settings

celery_app = Celery(
    "admetrics",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["celery_app.tasks"],
)

celery_app.conf.update(
    timezone="UTC",
    beat_schedule={
        "log_timestamp": {
            "task": "celery_app.tasks.log_timestamp_task",
            "schedule": crontab(minute="0", hour="*/1"),  # Run every 30 seconds
        },
    },
)
