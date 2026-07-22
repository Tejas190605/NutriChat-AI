from typing import Any

import structlog
from fastapi import APIRouter, Depends, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.db.session import get_async_session
from src.services.celery_app import celery_app
from src.services.redis_client import check_redis_health

logger = structlog.get_logger()
router = APIRouter()


def check_celery_workers() -> bool:
    """Helper function performing synchronous socket check to active workers.

    Runs inside a threadpool worker thread to prevent event loop starvation.
    """
    try:
        inspect_res = celery_app.control.inspect(timeout=1.0)
        workers_ping = inspect_res.ping() if inspect_res else None
        return bool(workers_ping)
    except Exception as e:
        logger.warning("Celery workers inspect check failed", error=str(e))
        return False


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Assess system operational health status",
)
async def health_check(
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, Any]:
    """Performs non-blocking operational health diagnostics on downstream systems."""

    # 1. Database Health check
    db_healthy = False
    try:
        await db.execute(text("SELECT 1"))
        db_healthy = True
    except Exception as e:
        logger.error("PostgreSQL connection check failed", error=str(e))

    # 2. Redis Caching Health check (async execution)
    redis_healthy = await check_redis_health()

    # 3. Celery Worker Queue check (threadpool isolation)
    celery_healthy = await run_in_threadpool(check_celery_workers)

    overall_healthy = db_healthy and redis_healthy

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "details": {
            "postgres": "connected" if db_healthy else "disconnected",
            "redis": "connected" if redis_healthy else "disconnected",
            "celery": "connected" if celery_healthy else "disconnected/unreachable",
        },
    }
