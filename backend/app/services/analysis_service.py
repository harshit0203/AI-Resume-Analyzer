"""Analysis orchestration: runs the multi-agent workflow and persists results."""
from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.workflow import AGENT_SEQUENCE, run_workflow
from app.core.exceptions import NotFoundError, ValidationError
from app.core.logging import get_logger
from app.models.agent_execution import AgentExecution
from app.models.analysis import Analysis
from app.models.career_insight import CareerInsight
from app.models.enums import (
    AgentStatus,
    AgentType,
    AnalysisStatus,
    ResumeStatus,
)
from app.models.job_match import JobMatch
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.resume_repository import ResumeRepository
from app.services.realtime import connection_manager

logger = get_logger(__name__)


def _clip(value: Any, max_len: int) -> str | None:
    """Trim a value to fit a bounded VARCHAR column (None-safe)."""
    if value is None:
        return None
    return str(value)[:max_len]


class AnalysisService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.analyses = AnalysisRepository(session)
        self.resumes = ResumeRepository(session)

    async def create(self, user_id: uuid.UUID, resume_id: uuid.UUID, target_role: str | None) -> Analysis:
        resume = await self.resumes.get_owned(resume_id, user_id)
        if resume is None:
            raise NotFoundError("Resume not found.")
        if resume.status != ResumeStatus.PARSED or not resume.raw_text:
            raise ValidationError("Resume has not been parsed successfully yet.")

        analysis = await self.analyses.create(
            user_id=user_id,
            resume_id=resume_id,
            target_role=target_role,
            status=AnalysisStatus.PENDING,
        )
        # Pre-create agent execution rows so the UI can render a full timeline.
        for index, agent_type in enumerate(AGENT_SEQUENCE):
            self.session.add(
                AgentExecution(
                    analysis_id=analysis.id,
                    agent_type=agent_type,
                    sequence=index,
                    status=AgentStatus.PENDING,
                )
            )
        await self.session.flush()
        return analysis

    async def run(self, analysis_id: uuid.UUID) -> Analysis:
        """Execute the workflow for a previously created analysis."""
        analysis = await self.analyses.get_detail_unscoped(analysis_id)
        if analysis is None:
            raise NotFoundError("Analysis not found.")
        resume = await self.resumes.get(analysis.resume_id)
        if resume is None or not resume.raw_text:
            raise ValidationError("Associated resume is missing parsed text.")

        executions = {e.agent_type: e for e in analysis.agent_executions}
        timings: dict[AgentType, float] = {}
        analysis_key = str(analysis.id)

        analysis.status = AnalysisStatus.RUNNING
        analysis.started_at = datetime.now(timezone.utc)
        await self.session.flush()
        await connection_manager.broadcast(analysis_key, {
            "type": "analysis_started",
            "analysis_id": analysis_key,
            "agents": [a.value for a in AGENT_SEQUENCE],
        })

        async def on_event(agent_value: str, status: str, data: dict[str, Any] | None) -> None:
            agent_type = AgentType(agent_value)
            execution = executions.get(agent_type)
            now = datetime.now(timezone.utc)
            if execution is not None:
                if status == "running":
                    execution.status = AgentStatus.RUNNING
                    execution.started_at = now
                    timings[agent_type] = time.perf_counter()
                elif status == "completed":
                    execution.status = AgentStatus.COMPLETED
                    execution.completed_at = now
                    execution.output = data
                    if agent_type in timings:
                        execution.duration_ms = round((time.perf_counter() - timings[agent_type]) * 1000, 2)
                elif status == "failed":
                    execution.status = AgentStatus.FAILED
                    execution.error = (data or {}).get("error")
                await self.session.flush()

            await connection_manager.broadcast(analysis_key, {
                "type": "agent_update",
                "analysis_id": analysis_key,
                "agent": agent_value,
                "status": status,
                "sequence": execution.sequence if execution else None,
                "data": data if status == "completed" else None,
            })

        started = time.perf_counter()
        try:
            final_state = await run_workflow(resume.raw_text, analysis.target_role, on_event)
            await self._persist_results(analysis, final_state)
            analysis.status = AnalysisStatus.COMPLETED
            analysis.completed_at = datetime.now(timezone.utc)
            analysis.duration_ms = round((time.perf_counter() - started) * 1000, 2)
            await self.session.flush()
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Analysis %s failed", analysis_id)
            # A failed flush poisons the current transaction, so roll back and
            # re-load the analysis before recording the failure — otherwise the
            # status stays RUNNING forever and clients poll indefinitely.
            await self.session.rollback()
            analysis = await self.analyses.get_detail_unscoped(analysis_id)
            if analysis is not None:
                analysis.status = AnalysisStatus.FAILED
                analysis.error = str(exc)[:2000]
                analysis.completed_at = datetime.now(timezone.utc)
                analysis.duration_ms = round((time.perf_counter() - started) * 1000, 2)
                await self.session.flush()

        status_value = analysis.status.value if analysis else AnalysisStatus.FAILED.value
        await connection_manager.broadcast(analysis_key, {
            "type": "analysis_completed",
            "analysis_id": analysis_key,
            "status": status_value,
            "ats_score": analysis.ats_score if analysis else None,
            "overall_score": analysis.overall_score if analysis else None,
        })
        return analysis

    async def _persist_results(self, analysis: Analysis, state: dict[str, Any]) -> None:
        ats = state.get("ats_result") or {}
        skill_gap = state.get("skill_gap_result") or {}
        improvement = state.get("improvement_result") or {}
        career = state.get("career_insight") or {}
        matches = state.get("job_matches") or []

        analysis.ats_result = ats
        analysis.skill_gap_result = skill_gap
        analysis.improvement_result = improvement
        analysis.ats_score = float(ats.get("ats_score", 0.0))

        coverage = float(skill_gap.get("coverage_percentage", 0.0))
        analysis.overall_score = round((analysis.ats_score * 0.6) + (coverage * 0.4), 1)
        analysis.summary = career.get("narrative")

        for match in matches:
            self.session.add(JobMatch(
                analysis_id=analysis.id,
                title=str(match.get("title", "Role"))[:255],
                company_type=_clip(match.get("company_type"), 255),
                match_percentage=float(match.get("match_percentage", 0.0)),
                seniority=_clip(match.get("seniority"), 64),
                salary_range=_clip(match.get("salary_range"), 128),
                reasons=match.get("reasons", []),
                missing_skills=match.get("missing_skills", []),
                matched_skills=match.get("matched_skills", []),
                description=match.get("description"),
            ))

        if career:
            self.session.add(CareerInsight(
                analysis_id=analysis.id,
                current_level=career.get("current_level"),
                target_role=career.get("target_role"),
                salary_insights=career.get("salary_insights"),
                next_steps=career.get("next_steps", []),
                recommended_certifications=career.get("recommended_certifications", []),
                learning_plan=career.get("learning_plan", []),
                growth_recommendations=career.get("growth_recommendations", []),
                roadmap=career.get("roadmap", []),
                narrative=career.get("narrative"),
            ))
        await self.session.flush()

    async def get_detail(self, analysis_id: uuid.UUID, user_id: uuid.UUID) -> Analysis:
        analysis = await self.analyses.get_detail(analysis_id, user_id)
        if analysis is None:
            raise NotFoundError("Analysis not found.")
        return analysis

    async def list(
        self, user_id: uuid.UUID, *, offset: int, limit: int, resume_id: uuid.UUID | None
    ) -> tuple[list[Analysis], int]:
        return await self.analyses.list_for_user(user_id, offset=offset, limit=limit, resume_id=resume_id)

    async def stats(self, user_id: uuid.UUID) -> dict[str, Any]:
        return await self.analyses.stats_for_user(user_id)

    async def delete(self, analysis_id: uuid.UUID, user_id: uuid.UUID) -> None:
        analysis = await self.analyses.get_detail(analysis_id, user_id)
        if analysis is None:
            raise NotFoundError("Analysis not found.")
        await self.analyses.delete(analysis)
