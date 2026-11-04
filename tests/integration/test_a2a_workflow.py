
"""Day 3: remote A2A workflow validation and failure handling."""

from unittest.mock import patch

from src.orchestrator.initial_state import create_initial_state
from src.orchestrator.supervisor import build_workflow


def run_a2a_workflow():
    """Run the deterministic workflow with remote A2A enabled."""
    workflow = build_workflow(
        mode="deterministic",
        use_a2a=True,
    )

    return workflow.invoke(
        create_initial_state(
            "Evaluate an enterprise multi-agent architecture"
        )
    )


def test_invalid_remote_assessment_is_rejected():
    """Invalid remote data must prevent workflow finalization."""
    invalid = {
        "request": "Evaluate architecture",
        "assessment": "Incomplete",
        "strengths": [],
        "risks": [],
        "recommendation": "",
    }

    with patch(
        "src.agents.remote_a2a.assess_remotely",
        return_value=invalid,
    ):
        result = run_a2a_workflow()

    # The remote A2A node rejects invalid data before Review.
    assert result["recommended_option"] == ""

    assert any(
        "Remote A2A Agent:" in error
        for error in result["errors"]
    )

    assert (
        "Remote A2A Agent: assessment failed"
        in result["execution_log"]
    )

    assert (
        "Supervisor: rejected recommendation"
        in result["execution_log"]
    )


def test_unavailable_remote_agent_rejects_workflow():
    """An unavailable remote service must prevent finalization."""
    with patch(
        "src.agents.remote_a2a.assess_remotely",
        side_effect=ConnectionError("A2A server unavailable"),
    ):
        result = run_a2a_workflow()

    assert result["recommended_option"] == ""

    assert any(
        "ConnectionError" in error
        for error in result["errors"]
    )

    assert (
        "Remote A2A Agent: assessment failed"
        in result["execution_log"]
    )

    assert (
        "Supervisor: rejected recommendation"
        in result["execution_log"]
    )
