"""Deterministic Review Agent for AI-A02."""

from pydantic import ValidationError

from src.contracts.models import ArchitectureAssessment
from src.orchestrator.state import WorkflowState
from src.a2a_server.assessment import AssessmentResponse


def review_agent(state: WorkflowState) -> dict:
    """Validate research and architecture assessments."""

    comments = []
    approved = True

    if not state["research_findings"]:
        comments.append("Research findings are missing")
        approved = False

    options = state["architecture_options"]

    if len(options) < 2:
        comments.append("At least two architecture options required")
        approved = False

    for index, option in enumerate(options, start=1):
        try:
            assessment = ArchitectureAssessment.model_validate(option)

            if not assessment.advantages:
                comments.append(f"Option {index}: advantages missing")
                approved = False

            if not assessment.operational_risks:
                comments.append(f"Option {index}: risks missing")
                approved = False

        except ValidationError:
            comments.append(f"Option {index}: invalid assessment schema")
            approved = False


    # Validate the remote A2A assessment when provided.
    remote = state.get("remote_assessment")

    if remote is not None:
        try:
            validated = AssessmentResponse.model_validate(remote)

            if (
                not validated.strengths
                or not validated.risks
                or not validated.recommendation.strip()
            ):
                comments.append("Remote A2A assessment is incomplete")
                approved = False
            else:
                comments.append("Remote A2A assessment passed validation")

        except (ValidationError, TypeError, ValueError):
            comments.append("Remote A2A assessment failed validation")
            approved = False


    if approved:
        comments.append("Architecture assessments passed review")

    return {
        "review_approved": approved,
        "review_comments": comments,
        "execution_log": state["execution_log"] + [
            f"Review Agent: {'approved' if approved else 'rejected'}"
        ],
    }
