"""FastAPI application entrypoint."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.v1.endpoints import websocket as websocket_endpoints
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware, SecurityHeadersMiddleware
from app.core.redis_client import close_redis, init_redis

configure_logging()
logger = get_logger("app.main")

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT] if settings.RATE_LIMIT_ENABLED else [],
    storage_uri=settings.REDIS_URL,
    enabled=settings.RATE_LIMIT_ENABLED,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s (%s)", settings.PROJECT_NAME, settings.ENVIRONMENT)
    await init_redis()
    yield
    await close_redis()
    logger.info("Shutdown complete.")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="Multi-agent AI resume analysis platform.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)
    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time-ms"],
    )

    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    # WebSocket mounted at root so the path is /ws/analyses/{id}.
    app.include_router(websocket_endpoints.router)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.PROJECT_NAME, "environment": settings.ENVIRONMENT}

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {"name": settings.PROJECT_NAME, "docs": "/docs", "version": "1.0.0"}

    return app


app = create_app()
