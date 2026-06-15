"""Job Match Agent: ranks suitable job roles for the candidate."""
from __future__ import annotations

from typing import Any

from app.agents.llm import LLMUnavailable, generate_json
from app.agents.skills_data import CAREER_PATHS, SALARY_BANDS


def _seniority(parsed: dict[str, Any]) -> str:
    years = parsed.get("total_experience_years") or 0
    if years >= 6:
        return "senior"
    if years >= 2:
        return "mid"
    return "junior"


def _heuristic_job_match(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    have = {s.lower() for s in parsed.get("skills", [])}
    level = _seniority(parsed)
    matches: list[dict[str, Any]] = []

    for role, required in CAREER_PATHS.items():
        matched = [s for s in required if s in have]
        missing = [s for s in required if s not in have]
        pct = round((len(matched) / len(required)) * 100, 1) if required else 0.0
        reasons = []
        if matched:
            reasons.append(f"You already have {len(matched)} of {len(required)} core skills.")
        if pct >= 70:
            reasons.append("Strong alignment with the role's core stack.")
        elif pct >= 40:
            reasons.append("Solid foundation with a few skills to close.")
        else:
            reasons.append("Emerging fit; targeted upskilling recommended.")
        matches.append({
            "title": role,
            "company_type": "Product & startups",
            "match_percentage": pct,
            "seniority": level,
            "salary_range": SALARY_BANDS.get(role, {}).get(level),
            "reasons": reasons,
            "matched_skills": matched,
            "missing_skills": missing,
            "description": f"{level.title()} {role} positions aligned with your profile.",
        })

    matches.sort(key=lambda m: m["match_percentage"], reverse=True)
    return matches[:6]


async def analyze_job_match(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        system = (
            "You are a technical recruiter. Return JSON {matches:[{title,company_type,"
            "match_percentage (0-100),seniority,salary_range,reasons[],matched_skills[],"
            "missing_skills[],description}]} with the 6 best-fit roles."
        )
        user = f"Candidate skills: {parsed.get('skills', [])}\nExperience years: {parsed.get('total_experience_years')}"
        result = await generate_json(system, user)
        matches = result.get("matches") if isinstance(result, dict) else None
        if matches:
            return matches[:6]
        return _heuristic_job_match(parsed)
    except LLMUnavailable:
        return _heuristic_job_match(parsed)
