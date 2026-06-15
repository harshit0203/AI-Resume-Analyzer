"""LangGraph multi-agent workflow orchestrating the full resume analysis.

Pipeline: parser -> ats -> skill_gap -> job_match -> improvement -> career_coach.
Each node emits ``running``/``completed``/``failed`` events through an optional
async callback so clients can observe progress in real time over WebSockets.
"""
from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.ats_agent import analyze_ats
from app.agents.career_coach_agent import analyze_career
from app.agents.improvement_agent import analyze_improvement
from app.agents.job_match_agent import analyze_job_match
from app.agents.parser_agent import parse_resume
from app.agents.skill_gap_agent import analyze_skill_gap
from app.agents.state import WorkflowState
from app.core.logging import get_logger
from app.models.enums import AgentType

logger = get_logger(__name__)

# Ordered list used to drive UI timelines and progress percentages.
AGENT_SEQUENCE: list[AgentType] = [
    AgentType.PARSER,
    AgentType.ATS,
    AgentType.SKILL_GAP,
    AgentType.JOB_MATCH,
    AgentType.IMPROVEMENT,
    AgentType.CAREER_COACH,
]


async def _emit(state: WorkflowState, agent: AgentType, status: str, data: dict[str, Any] | None = None) -> None:
    callback = state.get("on_event")
    if callback is not None:
        await callback(agent.value, status, data)


async def parser_node(state: WorkflowState) -> WorkflowState:
    await _emit(state, AgentType.PARSER, "running")
    try:
        parsed = await parse_resume(state["raw_text"])
        await _emit(state, AgentType.PARSER, "completed", parsed)
        return {"parsed": parsed}
    except Exception as exc:  # pragma: no cover
        logger.exception("Parser agent failed")
        await _emit(state, AgentType.PARSER, "failed", {"error": str(exc)})
        return {"parsed": {}, "errors": {**state.get("errors", {}), "parser": str(exc)}}


async def ats_node(state: WorkflowState) -> WorkflowState:
    await _emit(state, AgentType.ATS, "running")
    result = await analyze_ats(state.get("parsed", {}), state.get("raw_text", ""), state.get("target_role"))
    await _emit(state, AgentType.ATS, "completed", result)
    return {"ats_result": result}


async def skill_gap_node(state: WorkflowState) -> WorkflowState:
    await _emit(state, AgentType.SKILL_GAP, "running")
    result = await analyze_skill_gap(state.get("parsed", {}), state.get("target_role"))
    await _emit(state, AgentType.SKILL_GAP, "completed", result)
    return {"skill_gap_result": result}


async def job_match_node(state: WorkflowState) -> WorkflowState:
    await _emit(state, AgentType.JOB_MATCH, "running")
    matches = await analyze_job_match(state.get("parsed", {}))
    await _emit(state, AgentType.JOB_MATCH, "completed", {"matches": matches})
    return {"job_matches": matches}


async def improvement_node(state: WorkflowState) -> WorkflowState:
    await _emit(state, AgentType.IMPROVEMENT, "running")
    result = await analyze_improvement(state.get("parsed", {}), state.get("ats_result", {}))
    await _emit(state, AgentType.IMPROVEMENT, "completed", result)
    return {"improvement_result": result}


async def career_node(state: WorkflowState) -> WorkflowState:
    await _emit(state, AgentType.CAREER_COACH, "running")
    result = await analyze_career(
        state.get("parsed", {}), state.get("skill_gap_result", {}), state.get("target_role")
    )
    await _emit(state, AgentType.CAREER_COACH, "completed", result)
    return {"career_insight": result}


def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("parser", parser_node)
    graph.add_node("ats", ats_node)
    graph.add_node("skill_gap", skill_gap_node)
    graph.add_node("job_match", job_match_node)
    graph.add_node("improvement", improvement_node)
    graph.add_node("career", career_node)

    graph.add_edge(START, "parser")
    graph.add_edge("parser", "ats")
    graph.add_edge("ats", "skill_gap")
    graph.add_edge("skill_gap", "job_match")
    graph.add_edge("job_match", "improvement")
    graph.add_edge("improvement", "career")
    graph.add_edge("career", END)
    return graph.compile()


# Compiled once at import time and reused across requests.
resume_workflow = build_workflow()


async def run_workflow(
    raw_text: str,
    target_role: str | None,
    on_event=None,
) -> WorkflowState:
    initial: WorkflowState = {
        "raw_text": raw_text,
        "target_role": target_role,
        "errors": {},
        "on_event": on_event,
    }
    return await resume_workflow.ainvoke(initial)
