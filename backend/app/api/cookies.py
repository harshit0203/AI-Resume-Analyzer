"""Helpers for setting and clearing auth cookies consistently.

Two cookies are used:
- ``ara_access_token``  : short-lived access token (browser convenience).
- ``ara_refresh_token`` : long-lived refresh token, httpOnly + secure.

Both are httpOnly so they are never exposed to JavaScript, mitigating XSS
token theft. The frontend also receives the access token in the JSON body for
Authorization-header based requests.
"""
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
