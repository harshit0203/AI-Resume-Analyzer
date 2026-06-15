"""Structured logging configuration with rotating file handlers."""
from __future__ import annotations

import json
import logging
import logging.handlers
import sys
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


class JsonFormatter(logging.Formatter):
    """Render log records as single-line JSON for structured ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        for key, value in getattr(record, "extra_fields", {}).items():
            payload[key] = value
        # Attach common contextual attributes when present.
        for attr in ("request_id", "user_id", "path", "method", "status_code", "duration_ms"):
            if hasattr(record, attr):
                payload[attr] = getattr(record, attr)
        return json.dumps(payload, default=str)


class ConsoleFormatter(logging.Formatter):
    """Human friendly console formatter used during development."""

    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def configure_logging() -> None:
    """Configure root logging handlers exactly once."""
    root = logging.getLogger()
    if getattr(root, "_ara_configured", False):
        return

    root.setLevel(settings.LOG_LEVEL.upper())

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        ConsoleFormatter() if not settings.is_production else JsonFormatter()
    )
    root.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(JsonFormatter())
    root.addHandler(file_handler)

    error_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JsonFormatter())
    root.addHandler(error_handler)

    # Reduce noise from third party libraries.
    for noisy in ("uvicorn.access", "sqlalchemy.engine", "httpx", "openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    root._ara_configured = True  # type: ignore[attr-defined]


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger."""
    return logging.getLogger(name)
