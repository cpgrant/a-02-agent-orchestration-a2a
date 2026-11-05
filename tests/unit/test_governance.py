"""Unit tests for AI-A02 governance policies."""

import pytest

from src.governance.policy import (
    PolicyDecision,
    evaluate_policy,
)


def test_permit_approved_workflow():
    result = evaluate_policy(
        review_approved=True,
        errors=[],
    )

    assert result.decision == PolicyDecision.PERMIT
    assert result.policy_id == "GOV-003"


def test_deny_rejected_review():
    result = evaluate_policy(
        review_approved=False,
        errors=[],
    )

    assert result.decision == PolicyDecision.DENY
    assert result.policy_id == "GOV-001"


def test_deny_workflow_errors():
    result = evaluate_policy(
        review_approved=True,
        errors=["Remote A2A service unavailable"],
    )

    assert result.decision == PolicyDecision.DENY


def test_require_human_approval():
    result = evaluate_policy(
        review_approved=True,
        errors=[],
        requires_human_approval=True,
    )

    assert result.decision == PolicyDecision.REQUIRE_APPROVAL
    assert result.policy_id == "GOV-002"


def test_errors_override_approval_request():
    result = evaluate_policy(
        review_approved=True,
        errors=["Validation failed"],
        requires_human_approval=True,
    )

    assert result.decision == PolicyDecision.DENY


def test_rejected_review_overrides_approval_request():
    result = evaluate_policy(
        review_approved=False,
        errors=[],
        requires_human_approval=True,
    )

    assert result.decision == PolicyDecision.DENY
