"""Tests for AI-A02 operational observability."""

import json
import logging

import pytest

from src.observability.workflow import (
    classify_outcome,
    run_observed_workflow,
)


def test_completed_outcome():
    assert classify_outcome({
        "policy_decision": "PERMIT",
        "recommended_option": "Local LLM",
        "errors": [],
    }) == "COMPLETED"


def test_rejected_outcome():
    assert classify_outcome({
        "policy_decision": "DENY",
        "errors": [],
    }) == "REJECTED"


def test_awaiting_approval_outcome():
    assert classify_outcome({
        "policy_decision": "REQUIRE_APPROVAL",
        "recommended_option": "",
        "errors": [],
    }) == "AWAITING_APPROVAL"


def test_error_outcome():
    assert classify_outcome({
        "errors": ["Agent failed"],
    }) == "REJECTED"


def test_unknown_outcome():
    assert classify_outcome({}) == "UNKNOWN"


def test_workflow_telemetry(caplog):
    class FakeWorkflow:
        def invoke(self, state):
            return {
                **state,
                "policy_decision": "PERMIT",
                "recommended_option": "Local LLM",
                "errors": [],
                "execution_log": ["Research completed"],
            }

    state = {"request_id": "test-123"}

    with caplog.at_level(logging.INFO, logger="ai_a02.workflow"):
        result, telemetry = run_observed_workflow(
            FakeWorkflow(), state, mode="deterministic"
        )

    assert telemetry["request_id"] == "test-123"
    assert telemetry["outcome"] == "COMPLETED"
    assert telemetry["duration_ms"] >= 0
    assert telemetry["step_count"] == 1

    events = [
        json.loads(record.message)
        for record in caplog.records
        if record.name == "ai_a02.workflow"
    ]

    assert len(events) == 1
    assert events[0]["event"] == "workflow_completed"
    assert events[0]["request_id"] == "test-123"


def test_workflow_exception_is_logged(caplog):
    class FailingWorkflow:
        def invoke(self, state):
            raise RuntimeError("Simulated workflow failure")

    with caplog.at_level(logging.ERROR, logger="ai_a02.workflow"):
        with pytest.raises(RuntimeError, match="Simulated workflow failure"):
            run_observed_workflow(
                FailingWorkflow(),
                {"request_id": "failure-123"},
                mode="deterministic",
            )

    assert any(
        '"event": "workflow_failed"' in record.message
        for record in caplog.records
    )
