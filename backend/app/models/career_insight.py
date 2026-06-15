from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.analysis import Analysis

class CareerInsight(Base):
    __tablename__ = "career_insights"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        unique=True,
    )

    current_level: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_role: Mapped[str | None] = mapped_column(Text, nullable=True)
    salary_insights: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    next_steps: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    recommended_certifications: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    learning_plan: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    growth_recommendations: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    roadmap: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    narrative: Mapped[str | None] = mapped_column(Text, nullable=True)

    analysis: Mapped["Analysis"] = relationship(back_populates="career_insight")
