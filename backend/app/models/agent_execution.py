"""AgentExecution model: per-agent execution record within an analysis."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AgentStatus, AgentType

if TYPE_CHECKING:
    from app.models.analysis import Analysis


class AgentExecution(Base):
    __tablename__ = "agent_executions"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    agent_type: Mapped[AgentType] = mapped_column(Enum(AgentType, name="agent_type"), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[AgentStatus] = mapped_column(
        Enum(AgentStatus, name="agent_status"), default=AgentStatus.PENDING, nullable=False
    )

    output: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    analysis: Mapped["Analysis"] = relationship(back_populates="agent_executions")
