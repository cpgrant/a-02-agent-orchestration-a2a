"""Factory for initial LangGraph workflow state."""

from uuid import uuid4

from src.orchestrator.state import WorkflowState


def create_initial_state(request: str) -> WorkflowState:
    if not request or not request.strip():
        raise ValueError("Architecture request cannot be empty")

    return WorkflowState(
        request_id=str(uuid4()),
        request=request,
        research_findings=[],
        architecture_options=[],
        review_approved=False,
        review_comments=[],
        recommended_option="",
        recommendation_rationale="",
        execution_log=[],
        errors=[],
    )
