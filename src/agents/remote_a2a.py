"""LangGraph node that delegates assessment over A2A."""

from scripts.a2a_client import assess_remotely
from src.orchestrator.state import WorkflowState


def remote_a2a_agent(state: WorkflowState) -> dict:
    """Request an assessment from the independent A2A service."""

    try:
        assessment = assess_remotely(state["request"])

        if not isinstance(assessment, dict):
            raise ValueError("Remote assessment must be an object")

        required = {
            "request",
            "assessment",
            "strengths",
            "risks",
            "recommendation",
        }

        if not required.issubset(assessment):
            raise ValueError("Remote assessment missing required fields")

        if (
            not isinstance(assessment["strengths"], list)
            or not assessment["strengths"]
            or not isinstance(assessment["risks"], list)
            or not assessment["risks"]
            or not isinstance(assessment["recommendation"], str)
            or not assessment["recommendation"].strip()
        ):
            raise ValueError("Remote assessment contains invalid content")

        return {
            "remote_assessment": assessment,
            "execution_log": state["execution_log"] + [
                "Remote A2A Agent: assessment completed"
            ],
        }

    except Exception as exc:
        return {
            "remote_assessment": {},
            "errors": state["errors"] + [
                f"Remote A2A Agent: {type(exc).__name__}: {exc}"
            ],
            "execution_log": state["execution_log"] + [
                "Remote A2A Agent: assessment failed"
            ],
        }
