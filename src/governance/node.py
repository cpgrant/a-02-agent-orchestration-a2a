"""LangGraph governance policy gate."""

from src.governance.policy import evaluate_policy
from src.orchestrator.state import WorkflowState


def governance_node(state: WorkflowState) -> dict:
    result = evaluate_policy(
        review_approved=state["review_approved"],
        errors=state["errors"],
        requires_human_approval=state.get(
            "requires_human_approval", False
        ),
    )

    return {
        "policy_decision": result.decision.value,
        "policy_reason": result.reason,
        "execution_log": state["execution_log"] + [
            f"Governance: {result.decision.value} ({result.policy_id})"
        ],
    }


def route_after_governance(state: WorkflowState) -> str:
    return {
        "PERMIT": "finalize",
        "DENY": "reject",
        "REQUIRE_APPROVAL": "hold",
    }[state["policy_decision"]]


def hold_node(state: WorkflowState) -> dict:
    """Stop the workflow pending human authorization."""
    return {
        "recommended_option": "",
        "execution_log": state["execution_log"] + [
            "Supervisor: awaiting human approval"
        ],
    }
