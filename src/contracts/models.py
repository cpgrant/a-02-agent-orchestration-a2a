"""AI-A02 application-level agent contracts.

These are internal models, not A2A protocol message schemas.
"""

from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from typing import Literal

class TaskStatus(str, Enum):
    CREATED = "created"
    VALIDATED = "validated"
    PLANNED = "planned"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    REVIEWING = "reviewing"
    RETRY_PENDING = "retry_pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class AgentTask(BaseModel):
    task_id: UUID = Field(default_factory=uuid4)
    agent_name: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    context: dict[str, str] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.CREATED


class AgentResult(BaseModel):
    task_id: UUID
    agent_name: str = Field(min_length=1)
    success: bool
    summary: str
    evidence: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class ArchitectureAssessment(BaseModel):
    option: Literal["Local LLM", "Managed Cloud AI"]
    advantages: list[str]
    disadvantages: list[str]
    estimated_cost: str
    operational_risks: list[str]
    governance_considerations: list[str]


class FinalRecommendation(BaseModel):
    request_id: UUID
    recommended_option: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    assessments: list[ArchitectureAssessment]
    evidence: list[str]
    risks: list[str]
    approval_required: bool = False
