from __future__ import annotations

from fastapi import Response

from app.core.config import settings

ACCESS_COOKIE = "ara_access_token"
REFRESH_COOKIE = settings.COOKIE_NAME

def _base_kwargs() -> dict:
    kwargs: dict = {
        "httponly": True,
        "secure": settings.COOKIE_SECURE,
        "samesite": settings.COOKIE_SAMESITE,
        "path": "/",
    }
    if settings.COOKIE_DOMAIN:
        kwargs["domain"] = settings.COOKIE_DOMAIN
    return kwargs

def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        ACCESS_COOKIE,
        access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        **_base_kwargs(),
    )
    response.set_cookie(
        REFRESH_COOKIE,
        refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        **_base_kwargs(),
    )

def set_access_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        ACCESS_COOKIE,
        access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        **_base_kwargs(),
    )

def clear_auth_cookies(response: Response) -> None:
    domain = settings.COOKIE_DOMAIN
    response.delete_cookie(ACCESS_COOKIE, path="/", domain=domain)
    response.delete_cookie(REFRESH_COOKIE, path="/", domain=domain)
