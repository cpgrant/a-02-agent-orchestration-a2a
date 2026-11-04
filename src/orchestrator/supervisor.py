"""LangGraph supervisor for AI-A02."""

from langgraph.graph import StateGraph, START, END

from src.orchestrator.state import WorkflowState
from src.agents.research import research_agent
from src.agents.analysis import analysis_agent
from src.agents.review import review_agent
from src.agents.research_llm import research_llm_agent
from src.agents.analysis_llm import analysis_llm_agent


def route_after_review(state: WorkflowState) -> str:
    """Route based on review outcome."""
    if state["review_approved"] and not state["errors"]:
        return "finalize"
    return "reject"


def route_on_errors(state: WorkflowState) -> str:
    """Route to rejection if an agent reports an error."""
    return "reject" if state["errors"] else "continue"



def finalize_node(state: WorkflowState) -> dict:
    """Produce the approved recommendation."""

    options = state["architecture_options"]

    # Demonstration-only decision rule.
    # This is not a real financial or technical ranking.
    selected = options[0]["option"]

    return {
        "recommended_option": selected,
        "recommendation_rationale": (
            "Illustrative recommendation based on the "
            "structured assessment. A production decision "
            "requires workload-specific benchmarks, costs, "
            "and governance review."
        ),
        "execution_log": state["execution_log"] + [
            "Supervisor: finalized recommendation"
        ],
    }


def reject_node(state: WorkflowState) -> dict:
    """Record rejected assessments without finalizing."""

    return {
        "errors": state["errors"] + [
            "Supervisor: architecture review rejected"
        ],
        "execution_log": state["execution_log"] + [
            "Supervisor: rejected recommendation"
        ],
    }


def build_workflow(mode: str = "deterministic"):
    """Build a workflow with selectable agent implementations."""

    if mode not in ("deterministic", "llm"):
        raise ValueError(f"Unsupported workflow mode: {mode}")

    research_node = (
        research_llm_agent if mode == "llm" else research_agent
    )
    analysis_node = (
        analysis_llm_agent if mode == "llm" else analysis_agent
    )

    graph = StateGraph(WorkflowState)

    graph.add_node("research", research_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("review", review_agent)
    graph.add_node("finalize", finalize_node)
    graph.add_node("reject", reject_node)

    graph.add_edge(START, "research")

    graph.add_conditional_edges(
        "research",
        route_on_errors,
        {"continue": "analysis", "reject": "reject"},
    )

    graph.add_conditional_edges(
        "analysis",
        route_on_errors,
        {"continue": "review", "reject": "reject"},
    )

    graph.add_conditional_edges(
        "review",
        route_after_review,
        {"finalize": "finalize", "reject": "reject"},
    )

    graph.add_edge("finalize", END)
    graph.add_edge("reject", END)

    return graph.compile()

