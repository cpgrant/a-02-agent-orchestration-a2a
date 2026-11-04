"""Shared state for the AI-A02 LangGraph workflow."""

from typing import NotRequired, TypedDict


class WorkflowState(TypedDict):
    request_id: str
    request: str

    research_findings: list[str]
    architecture_options: list[dict]
    review_approved: bool
    review_comments: list[str]

    # Day 3: optional remote A2A assessment.
    remote_assessment: NotRequired[dict]

    recommended_option: str
    recommendation_rationale: str

    execution_log: list[str]
    errors: list[str]