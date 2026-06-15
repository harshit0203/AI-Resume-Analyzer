"""LLM provider wrapper.

Provides a single helper for structured JSON generation via OpenAI (through
LangChain). When no API key is configured the helper raises ``LLMUnavailable``
so callers can fall back to the deterministic engine.
"""
from __future__ import annotations

import json
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMUnavailable(RuntimeError):
    """Raised when the LLM cannot be used (no key / library error)."""


def is_available() -> bool:
    return bool(settings.AI_ENABLED and settings.OPENAI_API_KEY)


def _client():
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=settings.OPENAI_TEMPERATURE,
        api_key=settings.OPENAI_API_KEY,
        timeout=60,
        max_retries=2,
    )


async def generate_json(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """Call the LLM and parse a JSON object from the response."""
    if not is_available():
        raise LLMUnavailable("OpenAI API key is not configured.")

    from langchain_core.messages import HumanMessage, SystemMessage

    messages = [
        SystemMessage(content=system_prompt + "\n\nRespond ONLY with valid minified JSON."),
        HumanMessage(content=user_prompt),
    ]
    try:
        response = await _client().ainvoke(messages)
    except Exception as exc:  # pragma: no cover - network dependent
        logger.warning("LLM call failed: %s", exc)
        raise LLMUnavailable(str(exc)) from exc

    content = response.content if isinstance(response.content, str) else str(response.content)
    return _extract_json(content)


def _extract_json(content: str) -> dict[str, Any]:
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content[content.find("{") :]
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end == -1:
        raise LLMUnavailable("LLM returned no JSON object.")
    try:
        return json.loads(content[start : end + 1])
    except json.JSONDecodeError as exc:
        raise LLMUnavailable(f"Failed to decode LLM JSON: {exc}") from exc
