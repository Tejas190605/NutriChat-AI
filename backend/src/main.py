import asyncio
import os
import time
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

import structlog
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.health import router as health_router
from src.api.legal import router as legal_router
from src.api.v1.ai import router as ai_router
from src.api.v1.analytics import router as analytics_router
from src.api.v1.auth import router as auth_router
from src.api.v1.meals import router as meals_router
from src.api.v1.nutrition import router as nutrition_router
from src.api.v1.orchestration import router as orchestration_router
from src.api.v1.users import router as users_router
from src.api.v1.vision import router as vision_router
from src.api.v1.whatsapp import router as whatsapp_router
from src.config.settings import settings
from src.core.logging_config import configure_logging

# Configure structured logging configurations
configure_logging()
logger = structlog.get_logger()


def run_db_migrations() -> None:
    """Applies pending database migrations cleanly on application startup."""
    try:
        logger.info("Executing database migrations on startup...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations executed successfully.")
    except Exception as e:
        logger.error("Database migration execution failed on startup", error=str(e))
        raise e


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """FastAPI application lifecycle managing startup database migrations."""
    await asyncio.to_thread(run_db_migrations)
    yield


# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="0.1.0",
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
    lifespan=lifespan,
)

# Configure CORS middleware rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Asynchronous HTTP middleware logging request durations and paths."""
    start_time = time.time()

    # Trace request route path variables
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        method=request.method,
        path=request.url.path,
    )

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        "HTTP request processed",
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2),
    )
    return response


# Mount API Routers
app.include_router(legal_router, tags=["Legal Compliance"])
app.include_router(health_router, prefix="/api/v1", tags=["Diagnostic"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(meals_router, prefix="/api/v1/meals", tags=["Meals"])
app.include_router(nutrition_router, prefix="/api/v1/nutrition", tags=["Nutrition"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI Data"])
app.include_router(orchestration_router, prefix="/api/v1/ai", tags=["AI Orchestration"])
app.include_router(vision_router, prefix="/api/v1/vision", tags=["Computer Vision"])
app.include_router(
    whatsapp_router, prefix="/api/v1/whatsapp", tags=["WhatsApp Webhook"]
)
app.include_router(
    analytics_router, prefix="/api/v1/analytics", tags=["Analytics & Coaching"]
)

# Mount static folder for serving mock local uploads
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root_redirect() -> dict[str, Any]:
    """Standard landing API confirmation status response."""
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "documentation": "/docs" if settings.ENV != "production" else "disabled",
    }
