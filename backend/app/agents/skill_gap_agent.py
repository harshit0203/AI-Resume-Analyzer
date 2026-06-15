"""Skill Gap Agent: compares resume skills against target career paths."""
from __future__ import annotations

from typing import Any

from app.agents.llm import LLMUnavailable, generate_json
from app.agents.skills_data import (
    CAREER_PATHS,
    DEFAULT_RESOURCES,
    LEARNING_RESOURCES,
)


def _resolve_path(target_role: str | None) -> str:
    if target_role and target_role in CAREER_PATHS:
        return target_role
    if target_role:
        lowered = target_role.lower()
        for path in CAREER_PATHS:
            if path.lower() in lowered or lowered in path.lower():
                return path
    return "Full Stack Engineer"


def _heuristic_skill_gap(parsed: dict[str, Any], target_role: str | None) -> dict[str, Any]:
    path = _resolve_path(target_role)
    required = CAREER_PATHS[path]
    have = {s.lower() for s in parsed.get("skills", [])}

    matched = [s for s in required if s in have]
    missing = [s for s in required if s not in have]
    coverage = round((len(matched) / len(required)) * 100, 1) if required else 0.0

    missing_items = [
        {
            "skill": skill,
            "importance": "high" if idx < 3 else "medium",
            "resources": LEARNING_RESOURCES.get(skill, DEFAULT_RESOURCES),
        }
        for idx, skill in enumerate(missing)
    ]

    roadmap = []
    for phase, group in (("Weeks 1-4", missing[:2]), ("Weeks 5-8", missing[2:4]), ("Weeks 9-12", missing[4:])):
        if group:
            roadmap.append({
                "phase": phase,
                "focus": ", ".join(group),
                "outcome": f"Build a project applying {', '.join(group)}.",
            })

    return {
        "target_path": path,
        "matched_skills": matched,
        "missing_skills": missing_items,
        "coverage_percentage": coverage,
        "learning_roadmap": roadmap,
    }


async def analyze_skill_gap(parsed: dict[str, Any], target_role: str | None) -> dict[str, Any]:
    try:
        system = (
            "You are a senior tech career mentor. Compare the candidate's skills to the "
            "target career path and return JSON: {target_path, matched_skills[], "
            "missing_skills[{skill,importance,resources[]}], coverage_percentage (0-100), "
            "learning_roadmap[{phase,focus,outcome}]}."
        )
        path = _resolve_path(target_role)
        user = f"Target path: {path}\nRequired skills: {CAREER_PATHS[path]}\nCandidate skills: {parsed.get('skills', [])}"
        result = await generate_json(system, user)
        result.setdefault("target_path", path)
        return result
    except LLMUnavailable:
        return _heuristic_skill_gap(parsed, target_role)
