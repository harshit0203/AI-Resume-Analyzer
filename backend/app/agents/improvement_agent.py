"""Resume Improvement Agent: rewrites and strengthens resume content."""
from __future__ import annotations

from typing import Any

from app.agents.llm import LLMUnavailable, generate_json


def _heuristic_improvement(parsed: dict[str, Any], ats: dict[str, Any]) -> dict[str, Any]:
    skills = parsed.get("skills", [])
    role_hint = ", ".join(skills[:3]) if skills else "software engineering"
    years = parsed.get("total_experience_years") or 0

    improved_summary = (
        f"Results-driven engineer with {int(years) or 'hands-on'} years of experience "
        f"specialising in {role_hint}. Proven track record of shipping production systems, "
        "collaborating across teams, and translating requirements into measurable impact."
    )

    stronger_bullets = []
    for exp in parsed.get("experience", [])[:3]:
        for highlight in (exp.get("highlights") or [])[:2]:
            stronger_bullets.append({
                "before": highlight,
                "after": f"Delivered {highlight.rstrip('.').lower()}, improving outcomes by a measurable margin.",
            })
    if not stronger_bullets:
        stronger_bullets = [{
            "before": "Worked on web applications.",
            "after": "Built and shipped responsive web applications, cutting load times by 30%.",
        }]

    return {
        "improved_summary": improved_summary,
        "stronger_bullets": stronger_bullets,
        "achievement_suggestions": [
            "Quantify impact with metrics (revenue, latency, users, cost).",
            "Highlight ownership of end-to-end features or systems.",
            "Showcase cross-functional collaboration and leadership.",
        ],
        "project_suggestions": [
            f"Build a portfolio project demonstrating {role_hint}.",
            "Open-source a reusable library and document it well.",
        ],
        "ats_keywords": ats.get("missing_keywords", [])[:10],
    }


async def analyze_improvement(parsed: dict[str, Any], ats: dict[str, Any]) -> dict[str, Any]:
    try:
        system = (
            "You are an expert resume writer. Return JSON {improved_summary, "
            "stronger_bullets[{before,after}], achievement_suggestions[], "
            "project_suggestions[], ats_keywords[]}."
        )
        user = f"Parsed resume: {parsed}\nATS findings: {ats}"
        return await generate_json(system, user)
    except LLMUnavailable:
        return _heuristic_improvement(parsed, ats)
