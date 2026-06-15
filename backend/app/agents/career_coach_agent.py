"""Career Coach Agent: salary insights, next steps and growth plan."""
from __future__ import annotations

from typing import Any

from app.agents.llm import LLMUnavailable, generate_json
from app.agents.skills_data import SALARY_BANDS


def _level(years: float | None) -> str:
    if not years:
        return "junior"
    if years >= 6:
        return "senior"
    if years >= 2:
        return "mid"
    return "junior"


def _heuristic_career(parsed: dict[str, Any], skill_gap: dict[str, Any], target_role: str | None) -> dict[str, Any]:
    years = parsed.get("total_experience_years")
    level = _level(years)
    path = skill_gap.get("target_path") or target_role or "Full Stack Engineer"
    band = SALARY_BANDS.get(path, {})
    missing = [m["skill"] if isinstance(m, dict) else m for m in skill_gap.get("missing_skills", [])]

    next_level = {"junior": "mid", "mid": "senior", "senior": "staff/lead"}[level]

    return {
        "current_level": level,
        "target_role": path,
        "salary_insights": {
            "current_band": band.get(level),
            "next_band": band.get("senior") if level != "senior" else "$200k+",
            "currency": "USD",
            "note": "Indicative ranges; vary by region, company tier and interview performance.",
        },
        "next_steps": [
            f"Close priority skill gaps: {', '.join(missing[:3]) or 'deepen current stack'}.",
            f"Target {next_level}-level scope: own larger systems and mentor peers.",
            "Ship 1–2 portfolio projects with measurable outcomes.",
        ],
        "recommended_certifications": skill_gap.get("learning_roadmap", []) and [
            "AWS Certified Solutions Architect",
            "Professional certification aligned with your target path",
        ] or ["Cloud or domain certification aligned with your target path"],
        "learning_plan": skill_gap.get("learning_roadmap", []),
        "growth_recommendations": [
            "Build a public presence (blog, GitHub, talks).",
            "Seek stretch projects that expand system-design exposure.",
            "Collect quantified wins for performance reviews and interviews.",
        ],
        "roadmap": [
            {"horizon": "0-3 months", "goal": f"Solidify {path} fundamentals and close top gaps."},
            {"horizon": "3-6 months", "goal": f"Operate confidently at {level} and pursue {next_level} scope."},
            {"horizon": "6-12 months", "goal": f"Promote to {next_level} or switch to a higher-tier company."},
        ],
        "narrative": (
            f"You're tracking as a {level} {path}. Focus the next quarter on closing "
            f"{len(missing)} skill gaps and demonstrating ownership to unlock {next_level} roles."
        ),
    }


async def analyze_career(parsed: dict[str, Any], skill_gap: dict[str, Any], target_role: str | None) -> dict[str, Any]:
    try:
        system = (
            "You are an elite tech career coach. Return JSON {current_level, target_role, "
            "salary_insights{}, next_steps[], recommended_certifications[], "
            "learning_plan[], growth_recommendations[], roadmap[{horizon,goal}], narrative}."
        )
        user = f"Parsed resume: {parsed}\nSkill gap: {skill_gap}\nTarget role: {target_role}"
        return await generate_json(system, user)
    except LLMUnavailable:
        return _heuristic_career(parsed, skill_gap, target_role)
