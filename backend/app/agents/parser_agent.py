"""Resume Parser Agent.

Extracts structured fields (contact, skills, education, experience,
certifications, projects) from raw resume text. Uses the LLM when available
and a robust regex/heuristic parser otherwise.
"""
from __future__ import annotations

import re
from typing import Any

from app.agents.llm import LLMUnavailable, generate_json
from app.agents.skills_data import SKILL_ALIASES

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
URL_RE = re.compile(r"(https?://[^\s]+|(?:www\.|linkedin\.com/|github\.com/)[^\s]+)", re.I)

SECTION_HEADERS = {
    "summary": ["summary", "objective", "profile", "about"],
    "skills": ["skills", "technical skills", "core competencies", "technologies"],
    "experience": ["experience", "work experience", "employment", "professional experience"],
    "education": ["education", "academic", "qualifications"],
    "projects": ["projects", "personal projects", "key projects"],
    "certifications": ["certifications", "certificates", "licenses"],
}

# Flatten the known-skill vocabulary for matching.
_KNOWN_SKILLS = sorted(set(SKILL_ALIASES.values()), key=len, reverse=True)


def normalise_skill(raw: str) -> str | None:
    token = raw.strip().lower().strip(".,;:•-")
    if not token:
        return None
    return SKILL_ALIASES.get(token, token if token in _KNOWN_SKILLS else None)


def extract_skills(text: str) -> list[str]:
    found: set[str] = set()
    lower = text.lower()
    for skill in _KNOWN_SKILLS:
        pattern = r"(?<![\w])" + re.escape(skill) + r"(?![\w])"
        if re.search(pattern, lower):
            found.add(skill)
    for alias, canonical in SKILL_ALIASES.items():
        if re.search(r"(?<![\w])" + re.escape(alias) + r"(?![\w])", lower):
            found.add(canonical)
    return sorted(found)


def _split_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    sections: dict[str, list[str]] = {}
    current = "header"
    sections[current] = []
    for line in lines:
        stripped = line.strip().lower()
        matched = None
        for key, headers in SECTION_HEADERS.items():
            if any(stripped == h or stripped.startswith(h + ":") or stripped == h.title().lower()
                   for h in headers) and len(stripped) < 40:
                matched = key
                break
        if matched:
            current = matched
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _estimate_experience_years(text: str) -> float | None:
    years = re.findall(r"(19|20)\d{2}", text)
    if len(years) >= 2:
        nums = sorted(int(y) for y in re.findall(r"(?:19|20)\d{2}", text))
        span = nums[-1] - nums[0]
        if 0 < span <= 50:
            return float(span)
    match = re.search(r"(\d+)\+?\s*years?", text.lower())
    if match:
        return float(match.group(1))
    return None


def quick_structure(text: str) -> dict[str, Any]:
    """Deterministic structured extraction used during upload."""
    sections = _split_sections(text)
    header = sections.get("header", "")
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    links = [u.rstrip(").,") for u in URL_RE.findall(text)]

    # Name heuristic: first non-empty header line without an email/phone.
    name = None
    for line in header.splitlines():
        clean = line.strip()
        if clean and not EMAIL_RE.search(clean) and not PHONE_RE.search(clean) and len(clean) < 60:
            name = clean
            break

    certifications = [
        ln.strip("•-* ").strip()
        for ln in sections.get("certifications", "").splitlines()
        if ln.strip()
    ]

    projects = []
    for block in re.split(r"\n(?=[A-Z])", sections.get("projects", "")):
        block = block.strip()
        if block:
            title = block.splitlines()[0].strip("•-* ")
            projects.append({"name": title[:120], "description": block[:400], "technologies": extract_skills(block)})

    return {
        "contact": {
            "name": name,
            "email": emails[0] if emails else None,
            "phone": phones[0].strip() if phones else None,
            "location": None,
            "links": list(dict.fromkeys(links))[:5],
        },
        "summary": sections.get("summary") or None,
        "skills": extract_skills(text),
        "education": _parse_education(sections.get("education", "")),
        "experience": _parse_experience(sections.get("experience", "")),
        "certifications": certifications[:15],
        "projects": projects[:10],
        "languages": [],
        "total_experience_years": _estimate_experience_years(text),
    }


def _parse_education(block: str) -> list[dict[str, Any]]:
    items = []
    for line in block.splitlines():
        line = line.strip("•-* ").strip()
        if len(line) > 4:
            items.append({"institution": line[:160], "degree": None, "field_of_study": None,
                          "start_date": None, "end_date": None, "grade": None})
    return items[:8]


def _parse_experience(block: str) -> list[dict[str, Any]]:
    items = []
    for chunk in re.split(r"\n(?=[A-Z])", block):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.splitlines()
        highlights = [ln.strip("•-* ").strip() for ln in lines[1:] if ln.strip()]
        items.append({
            "company": None,
            "title": lines[0].strip("•-* ")[:160],
            "start_date": None,
            "end_date": None,
            "location": None,
            "highlights": highlights[:6],
        })
    return items[:10]


async def parse_resume(raw_text: str) -> dict[str, Any]:
    """LLM-enhanced parse with deterministic fallback."""
    baseline = quick_structure(raw_text)
    try:
        system = (
            "You are an expert resume parser. Extract structured data from the resume. "
            "Return JSON with keys: contact{name,email,phone,location,links[]}, summary, "
            "skills[], education[{institution,degree,field_of_study,start_date,end_date,grade}], "
            "experience[{company,title,start_date,end_date,location,highlights[]}], "
            "certifications[], projects[{name,description,technologies[],link}], languages[], "
            "total_experience_years."
        )
        result = await generate_json(system, f"Resume text:\n{raw_text[:8000]}")
        # Merge: prefer LLM but guarantee skills coverage from deterministic pass.
        merged_skills = sorted(set(result.get("skills", [])) | set(baseline["skills"]))
        result["skills"] = merged_skills
        return result
    except LLMUnavailable:
        return baseline
