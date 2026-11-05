"""Structured operational events for AI-A02 workflows."""

import json
import logging
import time
from datetime import datetime, timezone

LOGGER = logging.getLogger("ai_a02.workflow")


def classify_outcome(state: dict) -> str:
    """Determine the terminal workflow outcome."""
    decision = state.get("policy_decision")

    if decision == "REQUIRE_APPROVAL":
        return "AWAITING_APPROVAL"

    if decision == "DENY" or state.get("errors"):
        return "REJECTED"

    if decision == "PERMIT" and state.get("recommended_option"):
        return "COMPLETED"

    return "UNKNOWN"


def run_observed_workflow(workflow, state: dict, *, mode: str) -> tuple:
    """Execute an existing LangGraph workflow and emit a JSON summary."""
    start = time.perf_counter()
    request_id = state.get("request_id", "unknown")

    try:
        result = workflow.invoke(state)
    except Exception:
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        LOGGER.exception(
            json.dumps({
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "event": "workflow_failed",
                "request_id": request_id,
                "mode": mode,
                "duration_ms": duration_ms,
                "outcome": "FAILED",
            })
        )
        raise

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    outcome = classify_outcome(result)

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": "workflow_completed",
        "request_id": result.get("request_id", request_id),
        "mode": mode,
        "duration_ms": duration_ms,
        "outcome": outcome,
        "policy_decision": result.get("policy_decision"),
        "error_count": len(result.get("errors", [])),
        "step_count": len(result.get("execution_log", [])),
    }

    LOGGER.info(json.dumps(event))
    return result, event
