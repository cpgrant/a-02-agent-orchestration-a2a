"""Integration tests for governance decisions in LangGraph."""

from src.orchestrator.initial_state import create_initial_state
from src.orchestrator.supervisor import build_workflow


def run_workflow(*, approval_required=False, request="Architecture assessment"):
    state = create_initial_state(request)
    state["requires_human_approval"] = approval_required
    return build_workflow(mode="deterministic").invoke(state)


def test_permit_finalizes():
    result = run_workflow()

    assert result["policy_decision"] == "PERMIT"
    assert result["recommended_option"] == "Local LLM"
    assert "Supervisor: finalized recommendation" in result["execution_log"]


def test_approval_required_holds():
    result = run_workflow(approval_required=True)

    assert result["policy_decision"] == "REQUIRE_APPROVAL"
    assert result["recommended_option"] == ""
    assert "Supervisor: awaiting human approval" in result["execution_log"]
    assert "Supervisor: finalized recommendation" not in result["execution_log"]


def test_rejected_review_denies():
    """A rejected review must produce DENY and block finalization."""
    from unittest.mock import patch

    with patch(
        "src.orchestrator.supervisor.review_agent",
        return_value={
            "review_approved": False,
            "review_comments": ["Architecture review rejected"],
            "execution_log": ["Review Agent: rejected"],
        },
    ):
        workflow = build_workflow(mode="deterministic")
        result = workflow.invoke(
            create_initial_state("Architecture assessment")
        )

    assert result["policy_decision"] == "DENY"
    assert result["recommended_option"] == ""
    assert "Supervisor: rejected recommendation" in result["execution_log"]