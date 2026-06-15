from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, TypedDict

ProgressCallback = Callable[[str, str, Optional[dict[str, Any]]], Awaitable[None]]

class WorkflowState(TypedDict, total=False):
    raw_text: str
    target_role: Optional[str]
    parsed: dict[str, Any]
    ats_result: dict[str, Any]
    skill_gap_result: dict[str, Any]
    job_matches: list[dict[str, Any]]
    improvement_result: dict[str, Any]
    career_insight: dict[str, Any]
    errors: dict[str, str]
    on_event: Optional[ProgressCallback]
