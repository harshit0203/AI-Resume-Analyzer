"""Resume and parsed-data schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import ResumeStatus
from app.schemas.common import ORMModel


class ContactInfo(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    links: list[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    grade: str | None = None


class ExperienceItem(BaseModel):
    company: str | None = None
    title: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    location: str | None = None
    highlights: list[str] = Field(default_factory=list)


class ProjectItem(BaseModel):
    name: str | None = None
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)
    link: str | None = None


class ParsedResume(BaseModel):
    contact: ContactInfo = Field(default_factory=ContactInfo)
    summary: str | None = None
    skills: list[str] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    experience: list[ExperienceItem] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    total_experience_years: float | None = None


class ResumePublic(ORMModel):
    id: uuid.UUID
    file_name: str
    content_type: str
    file_size: int
    status: ResumeStatus
    version: int
    is_primary: bool
    parsed_data: dict[str, Any] | None = None
    parse_error: str | None = None
    created_at: datetime
    updated_at: datetime


class ResumeListItem(ORMModel):
    id: uuid.UUID
    file_name: str
    content_type: str
    file_size: int
    status: ResumeStatus
    version: int
    is_primary: bool
    created_at: datetime
