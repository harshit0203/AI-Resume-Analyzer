from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, UnauthorizedError
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.user_settings import UserSettings
from app.repositories.user_repository import UserRepository, UserSettingsRepository
from app.schemas.auth import ChangePasswordRequest
from app.schemas.user import UserSettingsUpdate, UserUpdate

class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)
        self.settings_repo = UserSettingsRepository(session)

    async def update_profile(self, user: User, payload: UserUpdate) -> User:
        data = payload.model_dump(exclude_unset=True)
        return await self.users.update(user, **data)

    async def change_password(self, user: User, payload: ChangePasswordRequest) -> None:
        if not verify_password(payload.current_password, user.hashed_password):
            raise UnauthorizedError("Current password is incorrect.")
        await self.users.update(user, hashed_password=hash_password(payload.new_password))

    async def get_settings(self, user_id: uuid.UUID) -> UserSettings:
        settings_row = await self.settings_repo.get_for_user(user_id)
        if settings_row is None:
            settings_row = await self.settings_repo.create(user_id=user_id)
        return settings_row

    async def update_settings(
        self, user_id: uuid.UUID, payload: UserSettingsUpdate
    ) -> UserSettings:
        settings_row = await self.get_settings(user_id)
        data = payload.model_dump(exclude_unset=True)
        return await self.settings_repo.update(settings_row, **data)
