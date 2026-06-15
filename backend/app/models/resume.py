from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ResumeStatus

if TYPE_CHECKING:
    from app.models.analysis import Analysis
    from app.models.user import User

class Resume(Base):
    __tablename__ = "resumes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    file_name: Mapped[str] = mapped_column(String(512), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    content_type: Mapped[str] = mapped_column(String(128), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)

    status: Mapped[ResumeStatus] = mapped_column(
        Enum(ResumeStatus, name="resume_status"), default=ResumeStatus.UPLOADED, nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    parse_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="resumes")
    analyses: Mapped[list["Analysis"]] = relationship(
        back_populates="resume", cascade="all, delete-orphan"
    )
