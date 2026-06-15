"""UserSettings model: per-user preferences and configuration."""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=True,
    )

    theme: Mapped[str] = mapped_column(String(32), default="dark", nullable=False)
    default_target_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    product_updates: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    analysis_complete_alerts: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    locale: Mapped[str] = mapped_column(String(16), default="en", nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)

    user: Mapped["User"] = relationship(back_populates="settings")
