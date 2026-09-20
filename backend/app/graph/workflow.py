from typing import TypedDict

from backend.app.agents.analyst import analyze
from backend.app.agents.critic import critique_report
from backend.app.agents.planner import create_plan
from backend.app.agents.researcher import research
from backend.app.agents.writer import write_report
from backend.app.services.execution import track_agent_execution
from backend.app.services.revision import needs_revision

from langgraph.graph import END, START, StateGraph


class ResearchState(TypedDict, total=False):
    run_id: int
    query: str
    research_questions: list[str]
    sources: list[dict]
    analysis: str
    report: str
    critique: str
    revision_count: int


def planner_node(state: ResearchState) -> ResearchState:
    questions = track_agent_execution(
        run_id=state["run_id"],
        agent_name="planner",
        function=create_plan,
        query=state["query"],
    )

    return {
        "research_questions": questions
    }


def researcher_node(state: ResearchState) -> ResearchState:
    _, sources = track_agent_execution(
        run_id=state["run_id"],
        agent_name="researcher",
        function=research,
        query=state["query"],
        research_questions=state["research_questions"],
    )

    return {
        "sources": sources
    }


def analyst_node(state: ResearchState) -> ResearchState:
    analysis = track_agent_execution(
        run_id=state["run_id"],
        agent_name="analyst",
        function=analyze,
        query=state["query"],
        research_questions=state["research_questions"],
        sources=state["sources"],
    )

    return {
        "analysis": analysis
    }


def writer_node(state: ResearchState) -> ResearchState:
    report = track_agent_execution(
        run_id=state["run_id"],
        agent_name="writer",
        function=write_report,
        query=state["query"],
        analysis=state["analysis"],
    )

    return {
        "report": report,
        "revision_count": 0,
    }


def critic_node(state: ResearchState) -> ResearchState:
    critique = track_agent_execution(
        run_id=state["run_id"],
        agent_name="critic",
        function=critique_report,
        query=state["query"],
        analysis=state["analysis"],
        report=state["report"],
    )

    return {
        "critique": critique
    }


def revision_writer_node(state: ResearchState) -> ResearchState:
    report = track_agent_execution(
        run_id=state["run_id"],
        agent_name="revision_writer",
        function=write_report,
        query=state["query"],
        analysis=state["analysis"],
        critique=state["critique"],
    )

    return {
        "report": report,
        "revision_count": state.get("revision_count", 0) + 1,
    }


def critic_router(state: ResearchState) -> str:
    if (
        needs_revision(state["critique"])
        and state.get("revision_count", 0) < 1
    ):
        return "revise"

    return "finish"


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    graph.add_node("critic", critic_node)
    graph.add_node("revision_writer", revision_writer_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", "critic")

    graph.add_conditional_edges(
        "critic",
        critic_router,
        {
            "revise": "revision_writer",
            "finish": END,
        },
    )

    graph.add_edge("revision_writer", "critic")

    return graph.compile()


research_graph = build_research_graph()