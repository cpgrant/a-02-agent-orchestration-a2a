"""Tests for the AI-A02 LangGraph workflow."""

from unittest.mock import patch

from src.orchestrator.initial_state import create_initial_state
from src.orchestrator.supervisor import build_workflow


def test_workflow_completes():
    workflow = build_workflow()

    state = create_initial_state(
        "Evaluate local LLM versus managed cloud AI"
    )

    result = workflow.invoke(state)

    assert len(result["research_findings"]) == 4
    assert len(result["architecture_options"]) == 2
    assert result["review_approved"] is True
    assert result["recommended_option"] == "Local LLM"
    assert result["errors"] == []


def test_workflow_execution_order():
    workflow = build_workflow()
    state = create_initial_state("Architecture assessment")

    result = workflow.invoke(state)

    assert result["execution_log"] == [
        "Research Agent: completed evidence collection",
        "Analysis Agent: completed architecture comparison",
        "Review Agent: approved",
        "Governance: PERMIT (GOV-003)",
        "Supervisor: finalized recommendation",
    ]
    assert result["policy_decision"] == "PERMIT"

def test_workflow_rejection():
    """A rejected review must not produce a recommendation."""

    def reject_review(state):
        return {
            "review_approved": False,
            "review_comments": ["Assessment failed quality review"],
            "execution_log": state["execution_log"] + [
                "Review Agent: rejected"
            ],
        }

    with patch(
        "src.orchestrator.supervisor.review_agent",
        reject_review,
    ):
        workflow = build_workflow()

    state = create_initial_state("Architecture assessment")
    result = workflow.invoke(state)

    assert result["review_approved"] is False
    assert result["recommended_option"] == ""
    assert "Supervisor: architecture review rejected" in result["errors"]
    assert result["execution_log"][-1] == (
        "Supervisor: rejected recommendation"
    )


def test_empty_request_rejected():
    try:
        create_initial_state("")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_analysis_failure_skips_review():
    """Analysis failure must bypass Review and route to Reject."""

    def failing_analysis(state):
        return {
            "errors": state["errors"] + [
                "Simulated analysis failure"
            ],
            "execution_log": state["execution_log"] + [
                "Analysis Agent: failed"
            ],
        }

    with patch(
        "src.orchestrator.supervisor.analysis_agent",
        failing_analysis,
    ):
        workflow = build_workflow()

    state = create_initial_state(
        "Evaluate local LLM versus managed cloud AI"
    )

    result = workflow.invoke(state)

    assert "Simulated analysis failure" in result["errors"]
    assert result["review_approved"] is False
    assert result["recommended_option"] == ""

    assert "Analysis Agent: failed" in result["execution_log"]
    assert not any(
        "Review Agent:" in entry
        for entry in result["execution_log"]
    )
    assert result["execution_log"][-1] == (
        "Supervisor: rejected recommendation"
    )
