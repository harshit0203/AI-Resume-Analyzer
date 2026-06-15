from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import ChangePasswordRequest
from app.schemas.common import APIResponse, MessageResponse
from app.schemas.user import (
    UserPublic,
    UserSettingsSchema,
    UserSettingsUpdate,
    UserUpdate,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=APIResponse[UserPublic])
async def get_profile(user: User = Depends(get_current_user)) -> APIResponse[UserPublic]:
    return APIResponse(data=UserPublic.model_validate(user))

@router.patch("/me", response_model=APIResponse[UserPublic])
async def update_profile(
    payload: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserPublic]:
    updated = await UserService(db).update_profile(user, payload)
    return APIResponse(data=UserPublic.model_validate(updated), message="Profile updated.")

@router.post("/me/change-password", response_model=MessageResponse)
async def change_password(
    payload: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    await UserService(db).change_password(user, payload)
    return MessageResponse(message="Password changed successfully.")

@router.get("/me/settings", response_model=APIResponse[UserSettingsSchema])
async def get_settings(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserSettingsSchema]:
    settings_row = await UserService(db).get_settings(user.id)
    return APIResponse(data=UserSettingsSchema.model_validate(settings_row))

@router.patch("/me/settings", response_model=APIResponse[UserSettingsSchema])
async def update_settings(
    payload: UserSettingsUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserSettingsSchema]:
    settings_row = await UserService(db).update_settings(user.id, payload)
    return APIResponse(data=UserSettingsSchema.model_validate(settings_row), message="Settings updated.")
