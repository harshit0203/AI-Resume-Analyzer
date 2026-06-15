"""User and settings schemas."""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import SubscriptionPlan, UserRole
from app.schemas.common import ORMModel


class UserPublic(ORMModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    avatar_url: str | None = None
    headline: str | None = None
    role: UserRole
    plan: SubscriptionPlan
    is_active: bool
    is_verified: bool
    last_login_at: datetime | None = None
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    headline: str | None = Field(default=None, max_length=255)
    avatar_url: str | None = Field(default=None, max_length=512)


class UserSettingsSchema(ORMModel):
    theme: str
    default_target_role: str | None = None
    email_notifications: bool
    product_updates: bool
    analysis_complete_alerts: bool
    locale: str
    timezone: str


class UserSettingsUpdate(BaseModel):
    theme: str | None = Field(default=None, max_length=32)
    default_target_role: str | None = Field(default=None, max_length=255)
    email_notifications: bool | None = None
    product_updates: bool | None = None
    analysis_complete_alerts: bool | None = None
    locale: str | None = Field(default=None, max_length=16)
    timezone: str | None = Field(default=None, max_length=64)
