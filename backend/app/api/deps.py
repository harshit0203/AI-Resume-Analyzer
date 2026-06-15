from __future__ import annotations

import uuid

from fastapi import Cookie, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)

async def get_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token: str | None = None
    if credentials is not None and credentials.scheme.lower() == "bearer":
        token = credentials.credentials
    if token is None:
        token = request.cookies.get("ara_access_token")
    if not token:
        raise UnauthorizedError("Authentication credentials were not provided.")

    payload = decode_token(token, "access")
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid access token.")

    user = await UserRepository(db).get(uuid.UUID(user_id))
    if user is None or not user.is_active:
        raise UnauthorizedError("User account is unavailable.")
    return user

async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.ADMIN:
        raise ForbiddenError("Administrator privileges are required.")
    return user
