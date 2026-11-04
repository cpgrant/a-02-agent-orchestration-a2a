"""Deterministic architecture assessment for the remote A2A agent."""

from pydantic import BaseModel, Field


class AssessmentResponse(BaseModel):
    request: str = Field(min_length=1)
    assessment: str
    strengths: list[str]
    risks: list[str]
    recommendation: str


def assess_architecture(request: str) -> AssessmentResponse:
    """Return an illustrative assessment without calling an LLM."""
    if not request.strip():
        raise ValueError("Assessment request must not be empty")

    return AssessmentResponse(
        request=request,
        assessment="Preliminary architecture assessment",
        strengths=[
            "Clear separation between orchestration and agent execution",
            "Supports independent deployment of specialist agents",
        ],
        risks=[
            "Remote-agent availability and network failures",
            "Authentication, authorization, and audit requirements",
        ],
        recommendation=(
            "Validate the A2A communication boundary, error handling, "
            "and governance controls before production deployment."
        ),
    )
