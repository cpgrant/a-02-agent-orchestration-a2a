"""Structured LLM output contracts."""

from pydantic import BaseModel, Field


class ResearchFindings(BaseModel):
    findings: list[str] = Field(min_length=3, max_length=6)
    assumptions: list[str] = Field(default_factory=list)
    information_gaps: list[str] = Field(default_factory=list)
