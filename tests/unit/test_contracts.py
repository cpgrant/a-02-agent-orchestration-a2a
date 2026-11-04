from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.contracts.models import (
    AgentTask,
    AgentResult,
    ArchitectureAssessment,
    FinalRecommendation,
    TaskStatus,
)


def test_agent_task_defaults():
    task = AgentTask(
        agent_name="research",
        objective="Evaluate LLM deployment options",
    )

    assert task.status == TaskStatus.CREATED
    assert task.context == {}
    assert task.task_id is not None


def test_agent_task_json_roundtrip():
    task = AgentTask(
        agent_name="analysis",
        objective="Compare architecture options",
    )

    restored = AgentTask.model_validate_json(
        task.model_dump_json()
    )

    assert restored == task


def test_agent_task_rejects_empty_agent():
    with pytest.raises(ValidationError):
        AgentTask(
            agent_name="",
            objective="Evaluate architecture",
        )


def test_agent_result():
    task_id = uuid4()

    result = AgentResult(
        task_id=task_id,
        agent_name="research",
        success=True,
        summary="Evidence collected",
        evidence=["Internal benchmark"],
    )

    assert result.success
    assert result.task_id == task_id


def test_architecture_assessment():
    assessment = ArchitectureAssessment(
        option="Local LLM",
        advantages=["Data control"],
        disadvantages=["Infrastructure cost"],
        estimated_cost="To be measured",
        operational_risks=["GPU availability"],
        governance_considerations=["Access control"],
    )

    assert assessment.option == "Local LLM"


def test_final_recommendation():
    recommendation = FinalRecommendation(
        request_id=uuid4(),
        recommended_option="Local LLM",
        rationale="Suitable for controlled workloads",
        assessments=[],
        evidence=["Benchmark results"],
        risks=["Operational overhead"],
    )

    assert recommendation.approval_required is False
    assert recommendation.recommended_option == "Local LLM"
