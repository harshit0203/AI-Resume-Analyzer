"""ATS Analyzer Agent: scores resume against ATS best practices."""
from __future__ import annotations

from typing import Any

from app.agents.llm import LLMUnavailable, generate_json
from app.agents.skills_data import ATS_KEYWORD_HINTS


def _heuristic_ats(parsed: dict[str, Any], raw_text: str) -> dict[str, Any]:
    text = (raw_text or "").lower()
    contact = parsed.get("contact", {})
    skills = parsed.get("skills", [])
    experience = parsed.get("experience", [])
    education = parsed.get("education", [])

    score = 40.0
    strengths: list[str] = []
    weaknesses: list[str] = []
    recommendations: list[str] = []
    formatting_issues: list[str] = []

    if contact.get("email"):
        score += 8
        strengths.append("Contact email is present and machine-readable.")
    else:
        weaknesses.append("No email detected by the parser.")
        recommendations.append("Add a clearly formatted email address near the top.")

    if contact.get("phone"):
        score += 5
    else:
        recommendations.append("Include a phone number for recruiter outreach.")

    if len(skills) >= 8:
        score += 14
        strengths.append(f"Strong, diverse skill set ({len(skills)} recognised skills).")
    elif len(skills) >= 4:
        score += 8
        recommendations.append("Expand the skills section with role-relevant keywords.")
    else:
        weaknesses.append("Few recognisable technical skills found.")
        recommendations.append("Add a dedicated, keyword-rich Skills section.")

    if experience:
        score += 12
        strengths.append("Work experience section detected.")
    else:
        weaknesses.append("No clearly delineated experience section.")

    if education:
        score += 6

    action_hits = sum(1 for kw in ATS_KEYWORD_HINTS if kw in text)
    if action_hits >= 5:
        score += 10
        strengths.append("Uses strong action verbs and measurable language.")
    else:
        recommendations.append("Start bullet points with quantified action verbs.")

    if any(ch.isdigit() for ch in text) and "%" in text:
        score += 5
        strengths.append("Includes quantified, metric-driven achievements.")
    else:
        recommendations.append("Quantify achievements with concrete metrics (%, $, time).")

    if len(text) < 800:
        formatting_issues.append("Resume appears short; ensure content was fully parsed.")

    missing_keywords = [kw for kw in ATS_KEYWORD_HINTS if kw not in text][:8]
    score = max(0.0, min(100.0, round(score, 1)))

    return {
        "ats_score": score,
        "strengths": strengths or ["Resume parsed successfully."],
        "weaknesses": weaknesses or ["No major weaknesses detected."],
        "missing_keywords": missing_keywords,
        "recommendations": recommendations or ["Tailor the resume to each target role."],
        "formatting_issues": formatting_issues,
    }


async def analyze_ats(parsed: dict[str, Any], raw_text: str, target_role: str | None) -> dict[str, Any]:
    try:
        system = (
            "You are an ATS (Applicant Tracking System) expert. Analyse the resume and "
            "return JSON: {ats_score (0-100 number), strengths[], weaknesses[], "
            "missing_keywords[], recommendations[], formatting_issues[]}."
        )
        user = f"Target role: {target_role or 'general'}\nParsed resume JSON:\n{parsed}"
        result = await generate_json(system, user)
        result.setdefault("ats_score", _heuristic_ats(parsed, raw_text)["ats_score"])
        result["ats_score"] = float(result["ats_score"])
        return result
    except LLMUnavailable:
        return _heuristic_ats(parsed, raw_text)
