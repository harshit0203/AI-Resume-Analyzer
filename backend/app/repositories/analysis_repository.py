"""Data access for analyses, agent executions, job matches and insights."""
from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.agent_execution import AgentExecution
from app.models.analysis import Analysis
from app.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Analysis, session)

    async def get_detail(self, analysis_id: uuid.UUID, user_id: uuid.UUID) -> Analysis | None:
        stmt = (
            select(Analysis)
            .where(Analysis.id == analysis_id, Analysis.user_id == user_id)
            .options(
                selectinload(Analysis.agent_executions),
                selectinload(Analysis.job_matches),
                selectinload(Analysis.career_insight),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_detail_unscoped(self, analysis_id: uuid.UUID) -> Analysis | None:
        stmt = (
            select(Analysis)
            .where(Analysis.id == analysis_id)
            .options(
                selectinload(Analysis.agent_executions),
                selectinload(Analysis.job_matches),
                selectinload(Analysis.career_insight),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_for_user(
        self,
        user_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
        resume_id: uuid.UUID | None = None,
    ) -> tuple[list[Analysis], int]:
        conditions = [Analysis.user_id == user_id]
        if resume_id:
            conditions.append(Analysis.resume_id == resume_id)
        base = select(Analysis).where(*conditions)
        total = await self.session.scalar(select(func.count()).select_from(base.subquery()))
        stmt = base.order_by(Analysis.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), int(total or 0)

    async def stats_for_user(self, user_id: uuid.UUID) -> dict[str, float | int]:
        total = await self.session.scalar(
            select(func.count()).select_from(Analysis).where(Analysis.user_id == user_id)
        )
        avg_ats = await self.session.scalar(
            select(func.avg(Analysis.ats_score)).where(
                Analysis.user_id == user_id, Analysis.ats_score.is_not(None)
            )
        )
        best_ats = await self.session.scalar(
            select(func.max(Analysis.ats_score)).where(Analysis.user_id == user_id)
        )
        return {
            "total_analyses": int(total or 0),
            "average_ats_score": round(float(avg_ats), 1) if avg_ats is not None else 0.0,
            "best_ats_score": round(float(best_ats), 1) if best_ats is not None else 0.0,
        }


class AgentExecutionRepository(BaseRepository[AgentExecution]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AgentExecution, session)
