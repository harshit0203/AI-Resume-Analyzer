"""Authentication business logic: registration, login and token rotation."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    needs_rehash,
    verify_password,
)
from app.models.user import User
from app.models.user_settings import UserSettings
from app.repositories.user_repository import UserRepository, UserSettingsRepository
from app.schemas.auth import LoginRequest, RegisterRequest

logger = get_logger(__name__)


class AuthService:
    """Coordinates user credential verification and JWT issuance."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.settings_repo = UserSettingsRepository(session)

    async def register(self, payload: RegisterRequest) -> User:
        email = payload.email.lower()
        if await self.users.email_exists(email):
            raise ConflictError("An account with this email already exists.")

        user = await self.users.create(
            email=email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name.strip(),
        )
        # Every user receives a settings row so the UI always has defaults.
        self.settings_repo.add(UserSettings(user_id=user.id))
        await self.session.flush()
        logger.info("Registered new user %s", user.id)
        return user

    async def authenticate(self, payload: LoginRequest) -> User:
        user = await self.users.get_by_email(payload.email.lower())
        # Constant-ish behaviour: always run a verify to reduce enumeration.
        if user is None:
            verify_password(payload.password, hash_password("dummy-password-123A"))
            raise UnauthorizedError("Invalid email or password.")
        if not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password.")
        if not user.is_active:
            raise ForbiddenError("This account has been deactivated.")

        # Opportunistically upgrade legacy/outdated hashes to current Argon2 params.
        if needs_rehash(user.hashed_password):
            user.hashed_password = hash_password(payload.password)

        user.last_login_at = datetime.now(timezone.utc)
        await self.session.flush()
        return user

    def issue_tokens(self, user: User) -> tuple[str, str]:
        claims = {"role": user.role.value, "email": user.email}
        access = create_access_token(str(user.id), claims)
        refresh = create_refresh_token(str(user.id), {"role": user.role.value})
        return access, refresh

    async def refresh(self, refresh_token: str) -> tuple[User, str]:
        payload = decode_token(refresh_token, "refresh")
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("Malformed refresh token.")
        user = await self.users.get(uuid.UUID(user_id))
        if user is None or not user.is_active:
            raise UnauthorizedError("User no longer exists or is inactive.")
        access = create_access_token(
            str(user.id), {"role": user.role.value, "email": user.email}
        )
        return user, access

    @staticmethod
    def access_token_max_age() -> int:
        return settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    @staticmethod
    def refresh_token_max_age() -> int:
        return settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
