"""Application configuration powered by Pydantic settings.

All configuration is sourced from environment variables (and an optional
`.env` file) so the application can be configured per-environment without
code changes.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Any, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly typed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------ App
    PROJECT_NAME: str = "AIResumeAnalyzer"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS origins (comma-separated string or list)
    CORS_ORIGINS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    # ------------------------------------------------------------- Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/airesume"
    DATABASE_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # ---------------------------------------------------------------- Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # -------------------------------------------------------------- Security
    JWT_SECRET_KEY: str = "change-me-in-production-access"
    JWT_REFRESH_SECRET_KEY: str = "change-me-in-production-refresh"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12

    # Cookie configuration for refresh tokens
    COOKIE_NAME: str = "ara_refresh_token"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    COOKIE_DOMAIN: str | None = None

    # --------------------------------------------------------------- OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.2
    AI_ENABLED: bool = True

    # ----------------------------------------------------------- File upload
    STORAGE_BACKEND: Literal["local", "s3"] = "local"
    UPLOAD_DIR: str = "storage/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_UPLOAD_EXTENSIONS: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: [".pdf", ".docx"]
    )

    # Optional S3 configuration
    S3_BUCKET: str | None = None
    S3_REGION: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    # --------------------------------------------------------- Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "200/minute"
    RATE_LIMIT_AUTH: str = "20/minute"

    @field_validator("CORS_ORIGINS", "ALLOWED_UPLOAD_EXTENSIONS", mode="before")
    @classmethod
    def _split_csv(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
