"""Shared state for the AI-A02 LangGraph workflow."""

from typing import TypedDict


class WorkflowState(TypedDict):
    request_id: str
    request: str

    research_findings: list[str]
    architecture_options: list[dict]
    review_approved: bool
    review_comments: list[str]

    recommended_option: str
    recommendation_rationale: str

    execution_log: list[str]
    errors: list[str]
