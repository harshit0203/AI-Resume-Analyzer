"""Domain and application level exceptions with structured handling."""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base class for all expected application errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "app_error"
    message: str = "An application error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        error_code: str | None = None,
        status_code: int | None = None,
        details: Any | None = None,
    ) -> None:
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        self.status_code = status_code or self.status_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    message = "The requested resource was not found."


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    error_code = "conflict"
    message = "The resource already exists."


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "unauthorized"
    message = "Authentication is required."


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "forbidden"
    message = "You do not have permission to perform this action."


class ValidationError(AppError):
    status_code = 422
    error_code = "validation_error"
    message = "The request payload failed validation."


class RateLimitError(AppError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "rate_limited"
    message = "Too many requests. Please slow down."


class ServiceUnavailableError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "service_unavailable"
    message = "An upstream service is currently unavailable."


def _error_payload(error_code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "success": False,
        "error": {"code": error_code, "message": message},
    }
    if details is not None:
        body["error"]["details"] = details
    return body


def register_exception_handlers(app: FastAPI) -> None:
    """Attach consistent JSON error responses to the FastAPI app."""

    @app.exception_handler(AppError)
    async def _handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        logger.warning("AppError: %s (%s)", exc.message, exc.error_code)
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(exc.error_code, exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _handle_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_payload(
                "validation_error",
                "Request validation failed.",
                details=exc.errors(),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload("http_error", str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def _handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_error_payload("internal_error", "An unexpected error occurred."),
        )
