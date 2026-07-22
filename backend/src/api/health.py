import structlog
from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.db.session import get_async_session
from src.services.celery_app import celery_app
from src.services.redis_client import check_redis_health

logger = structlog.get_logger()
router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Assess system operational health status",
)
async def health_check(db: AsyncSession = Depends(get_async_session)) -> dict[str, Any]:
    """Performs real-time diagnostic checks on db, cache, and Celery workers."""

    # 1. Database Health check
    db_healthy = False
    try:
        await db.execute(text("SELECT 1"))
        db_healthy = True
    except Exception as e:
        logger.error("PostgreSQL connection check failed", error=str(e))

    # 2. Redis Caching Health check
    redis_healthy = check_redis_health()

    # 3. Celery Worker Queue check
    celery_healthy = False
    try:
        inspect_res = celery_app.control.inspect(timeout=1.0)
        # Verify if any active worker responds to ping
        workers_ping = inspect_res.ping() if inspect_res else None
        if workers_ping:
            celery_healthy = True
    except Exception as e:
        logger.warning("Celery workers connection check unreachable", error=str(e))

    overall_healthy = db_healthy and redis_healthy

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "details": {
            "postgres": "connected" if db_healthy else "disconnected",
            "redis": "connected" if redis_healthy else "disconnected",
            "celery": "connected" if celery_healthy else "disconnected/unreachable",
        },
    }
