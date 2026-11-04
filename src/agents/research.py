"""Deterministic Research Agent for AI-A02."""

from src.orchestrator.state import WorkflowState


def research_agent(state: WorkflowState) -> dict:
    """Return research findings as a LangGraph state update."""

    findings = [
        "Local LLM deployment provides greater direct control "
        "over model hosting and data processing.",

        "Local deployment requires GPU capacity, infrastructure "
        "management, monitoring, and model maintenance.",

        "Managed cloud AI can reduce infrastructure management "
        "but introduces provider dependencies and usage-based costs.",

        "Both deployment models require access controls, "
        "security monitoring, evaluation, and governance.",
    ]

    return {
        "research_findings": findings,
        "execution_log": state["execution_log"] + [
            "Research Agent: completed evidence collection"
        ],
    }
