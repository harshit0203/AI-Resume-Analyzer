from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import AgentStatus, AgentType, AnalysisStatus
from app.schemas.common import ORMModel

class CreateAnalysisRequest(BaseModel):
    resume_id: uuid.UUID
    target_role: str | None = Field(default=None, max_length=255)

class ATSResult(BaseModel):
    ats_score: float = 0.0
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    formatting_issues: list[str] = Field(default_factory=list)

class SkillGapItem(BaseModel):
    skill: str
    importance: str = "medium"
    resources: list[str] = Field(default_factory=list)

class SkillGapResult(BaseModel):
    target_path: str | None = None
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[SkillGapItem] = Field(default_factory=list)
    coverage_percentage: float = 0.0
    learning_roadmap: list[dict[str, Any]] = Field(default_factory=list)

class JobMatchResult(BaseModel):
    title: str
    company_type: str | None = None
    match_percentage: float = 0.0
    seniority: str | None = None
    salary_range: str | None = None
    reasons: list[str] = Field(default_factory=list)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    description: str | None = None

class ImprovementResult(BaseModel):
    improved_summary: str | None = None
    stronger_bullets: list[dict[str, str]] = Field(default_factory=list)
    achievement_suggestions: list[str] = Field(default_factory=list)
    project_suggestions: list[str] = Field(default_factory=list)
    ats_keywords: list[str] = Field(default_factory=list)

class CareerInsightResult(BaseModel):
    current_level: str | None = None
    target_role: str | None = None
    salary_insights: dict[str, Any] = Field(default_factory=dict)
    next_steps: list[str] = Field(default_factory=list)
    recommended_certifications: list[str] = Field(default_factory=list)
    learning_plan: list[dict[str, Any]] = Field(default_factory=list)
    growth_recommendations: list[str] = Field(default_factory=list)
    roadmap: list[dict[str, Any]] = Field(default_factory=list)
    narrative: str | None = None

class AgentExecutionPublic(ORMModel):
    id: uuid.UUID
    agent_type: AgentType
    sequence: int
    status: AgentStatus
    output: dict[str, Any] | None = None
    error: str | None = None
    tokens_used: int | None = None
    duration_ms: float | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

class JobMatchPublic(ORMModel):
    id: uuid.UUID
    title: str
    company_type: str | None = None
    match_percentage: float
    seniority: str | None = None
    salary_range: str | None = None
    reasons: list[str]
    missing_skills: list[str]
    matched_skills: list[str]
    description: str | None = None

class CareerInsightPublic(ORMModel):
    id: uuid.UUID
    current_level: str | None = None
    target_role: str | None = None
    salary_insights: dict[str, Any] | None = None
    next_steps: list[str]
    recommended_certifications: list[str]
    learning_plan: list[dict[str, Any]]
    growth_recommendations: list[str]
    roadmap: list[dict[str, Any]]
    narrative: str | None = None

class AnalysisListItem(ORMModel):
    id: uuid.UUID
    resume_id: uuid.UUID
    status: AnalysisStatus
    target_role: str | None = None
    ats_score: float | None = None
    overall_score: float | None = None
    created_at: datetime
    completed_at: datetime | None = None

class AnalysisDetail(ORMModel):
    id: uuid.UUID
    resume_id: uuid.UUID
    status: AnalysisStatus
    target_role: str | None = None
    ats_score: float | None = None
    overall_score: float | None = None
    ats_result: dict[str, Any] | None = None
    skill_gap_result: dict[str, Any] | None = None
    improvement_result: dict[str, Any] | None = None
    summary: str | None = None
    error: str | None = None
    duration_ms: float | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    agent_executions: list[AgentExecutionPublic] = Field(default_factory=list)
    job_matches: list[JobMatchPublic] = Field(default_factory=list)
    career_insight: CareerInsightPublic | None = None
