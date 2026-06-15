"""Enumerations shared across models and schemas."""
from __future__ import annotations

import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class ResumeStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    FAILED = "failed"


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentType(str, enum.Enum):
    PARSER = "resume_parser"
    ATS = "ats_analyzer"
    SKILL_GAP = "skill_gap"
    JOB_MATCH = "job_match"
    IMPROVEMENT = "resume_improvement"
    CAREER_COACH = "career_coach"


class CareerPath(str, enum.Enum):
    MERN_DEVELOPER = "MERN Developer"
    FULLSTACK_ENGINEER = "Full Stack Engineer"
    AI_ENGINEER = "AI Engineer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    PYTHON_DEVELOPER = "Python Developer"
    JAVA_DEVELOPER = "Java Developer"
