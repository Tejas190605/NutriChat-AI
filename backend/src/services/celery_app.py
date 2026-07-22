from celery import Celery

from src.config.settings import settings

# Initialize Celery Application
celery_app = Celery(
    "nutrichat_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Standard queue settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
)


@celery_app.task(name="src.services.celery_app.test_celery_task")  # type: ignore[untyped-decorator]
def test_celery_task(x: int, y: int) -> int:
    """A baseline diagnostic Celery task that performs additions.

    Args:
        x: An integer input.
        y: Another integer input.

    Returns:
        The sum of x and y.
    """
    return x + y
