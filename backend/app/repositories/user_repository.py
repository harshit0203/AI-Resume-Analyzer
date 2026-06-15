"""Data access for users and their settings."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.user_settings import UserSettings
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None


class UserSettingsRepository(BaseRepository[UserSettings]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UserSettings, session)

    async def get_for_user(self, user_id: uuid.UUID) -> UserSettings | None:
        return await self.get_by(user_id=user_id)
