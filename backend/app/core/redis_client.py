"""Redis connection helper used for caching and rate limiting.

The client degrades gracefully: if Redis is unavailable the cache helpers
become no-ops so the application keeps functioning in local development.
"""
from __future__ import annotations

import json
from typing import Any

import redis.asyncio as aioredis

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_redis: aioredis.Redis | None = None


async def init_redis() -> None:
    """Initialise the global Redis connection pool."""
    global _redis
    try:
        _redis = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        await _redis.ping()
        logger.info("Connected to Redis at %s", settings.REDIS_URL)
    except Exception as exc:  # pragma: no cover - environment dependent
        logger.warning("Redis unavailable, caching disabled: %s", exc)
        _redis = None


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None


def get_redis() -> aioredis.Redis | None:
    return _redis


async def cache_get(key: str) -> Any | None:
    if _redis is None:
        return None
    try:
        raw = await _redis.get(key)
        return json.loads(raw) if raw else None
    except Exception as exc:  # pragma: no cover
        logger.warning("cache_get failed for %s: %s", key, exc)
        return None


async def cache_set(key: str, value: Any, ttl: int | None = None) -> None:
    if _redis is None:
        return
    try:
        await _redis.set(key, json.dumps(value, default=str), ex=ttl or settings.REDIS_CACHE_TTL)
    except Exception as exc:  # pragma: no cover
        logger.warning("cache_set failed for %s: %s", key, exc)


async def cache_delete(*keys: str) -> None:
    if _redis is None or not keys:
        return
    try:
        await _redis.delete(*keys)
    except Exception as exc:  # pragma: no cover
        logger.warning("cache_delete failed: %s", exc)
