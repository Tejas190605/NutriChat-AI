import time
from collections.abc import Awaitable, Callable
from typing import Any

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.api.health import router as health_router
from src.config.settings import settings
from src.core.logging_config import configure_logging

# Configure structured logging configurations
configure_logging()
logger = structlog.get_logger()

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="0.1.0",
    docs_url="/docs" if settings.ENV != "production" else None,
    redoc_url="/redoc" if settings.ENV != "production" else None,
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
app.include_router(health_router, prefix="/api/v1", tags=["Diagnostic"])


@app.get("/")
async def root_redirect() -> dict[str, Any]:
    """Standard landing API confirmation status response."""
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "documentation": "/docs" if settings.ENV != "production" else "disabled",
    }
