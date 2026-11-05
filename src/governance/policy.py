"""Deterministic governance policy evaluation for AI-A02."""

from enum import Enum

from pydantic import BaseModel, Field


class PolicyDecision(str, Enum):
    PERMIT = "PERMIT"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class PolicyResult(BaseModel):
    decision: PolicyDecision
    reason: str = Field(min_length=1)
    policy_id: str = Field(min_length=1)


def evaluate_policy(
    *,
    review_approved: bool,
    errors: list[str],
    requires_human_approval: bool = False,
) -> PolicyResult:
    """Apply explicit deterministic governance rules."""

    if errors or not review_approved:
        return PolicyResult(
            decision=PolicyDecision.DENY,
            reason="Review rejected or workflow errors detected",
            policy_id="GOV-001",
        )

    if requires_human_approval:
        return PolicyResult(
            decision=PolicyDecision.REQUIRE_APPROVAL,
            reason="Human approval required before finalization",
            policy_id="GOV-002",
        )

    return PolicyResult(
        decision=PolicyDecision.PERMIT,
        reason="Review passed and no additional approval required",
        policy_id="GOV-003",
    )
