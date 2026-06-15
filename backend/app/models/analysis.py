from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AnalysisStatus

if TYPE_CHECKING:
    from app.models.agent_execution import AgentExecution
    from app.models.career_insight import CareerInsight
    from app.models.job_match import JobMatch
    from app.models.resume import Resume
    from app.models.user import User

class Analysis(Base):
    __tablename__ = "analyses"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False
    )

    status: Mapped[AnalysisStatus] = mapped_column(
        Enum(AnalysisStatus, name="analysis_status"), default=AnalysisStatus.PENDING, nullable=False
    )
    target_role: Mapped[str | None] = mapped_column(String(255), nullable=True)

    ats_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    ats_result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    skill_gap_result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    improvement_result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship(back_populates="analyses")
    resume: Mapped["Resume"] = relationship(back_populates="analyses")
    agent_executions: Mapped[list["AgentExecution"]] = relationship(
        back_populates="analysis", cascade="all, delete-orphan", order_by="AgentExecution.sequence"
    )
    job_matches: Mapped[list["JobMatch"]] = relationship(
        back_populates="analysis", cascade="all, delete-orphan"
    )
    career_insight: Mapped["CareerInsight"] = relationship(
        back_populates="analysis", cascade="all, delete-orphan", uselist=False
    )
