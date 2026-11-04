"""LLM-mode workflow tests with mocked model responses."""

from unittest.mock import patch

from src.orchestrator.initial_state import create_initial_state
from src.orchestrator.supervisor import build_workflow


def mock_research(state):
    return {
        "research_findings": [
            "Local deployment offers infrastructure control.",
            "Managed services reduce hosting responsibilities.",
            "Both require enterprise governance.",
        ],
        "execution_log": state["execution_log"] + [
            "Research LLM Agent: completed"
        ],
    }


def mock_analysis(state):
    return {
        "architecture_options": [
            {
                "option": "Local LLM",
                "advantages": ["Data control"],
                "disadvantages": ["Infrastructure costs"],
                "estimated_cost": "TCO analysis required",
                "operational_risks": ["GPU capacity"],
                "governance_considerations": ["Access control"],
            },
            {
                "option": "Managed Cloud AI",
                "advantages": ["Managed infrastructure"],
                "disadvantages": ["Provider dependency"],
                "estimated_cost": "Pricing analysis required",
                "operational_risks": ["Service availability"],
                "governance_considerations": ["Data agreements"],
            },
        ],
        "execution_log": state["execution_log"] + [
            "Analysis LLM Agent: completed"
        ],
    }


def test_llm_workflow_with_mocked_agents():
    with (
        patch(
            "src.orchestrator.supervisor.research_llm_agent",
            mock_research,
        ),
        patch(
            "src.orchestrator.supervisor.analysis_llm_agent",
            mock_analysis,
        ),
    ):
        workflow = build_workflow(mode="llm")

    result = workflow.invoke(
        create_initial_state("Evaluate deployment options")
    )

    assert result["review_approved"] is True
    assert len(result["architecture_options"]) == 2
    assert result["errors"] == []
    assert result["recommended_option"] == "Local LLM"
    assert "Research LLM Agent: completed" in result["execution_log"]
    assert "Analysis LLM Agent: completed" in result["execution_log"]


def test_llm_failure_routes_to_rejection():
    def failing_research(state):
        return {
            "errors": state["errors"] + [
                "Simulated model failure"
            ],
            "execution_log": state["execution_log"] + [
                "Research LLM Agent: failed"
            ],
        }

    with patch(
        "src.orchestrator.supervisor.research_llm_agent",
        failing_research,
    ):
        workflow = build_workflow(mode="llm")

    result = workflow.invoke(
        create_initial_state("Evaluate deployment options")
    )

    assert result["review_approved"] is False
    assert result["recommended_option"] == ""
    assert "Simulated model failure" in result["errors"]
    assert not any(
        "Analysis LLM Agent:" in entry
        for entry in result["execution_log"]
    )
    assert result["execution_log"][-1] == (
        "Supervisor: rejected recommendation"
    )
