"""JobMatch model: matched job roles produced by the Job Match agent."""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.analysis import Analysis


class JobMatch(Base):
    __tablename__ = "job_matches"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    match_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    seniority: Mapped[str | None] = mapped_column(String(64), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(128), nullable=True)

    reasons: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    missing_skills: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    matched_skills: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    analysis: Mapped["Analysis"] = relationship(back_populates="job_matches")
