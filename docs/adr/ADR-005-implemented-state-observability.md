# ADR-005 — Implemented State and Observability

Status: Accepted
Date: 2026-11-05
Supersedes: ADR-004

## Context

ADR-004 proposed PostgreSQL persistence and OpenTelemetry
distributed tracing.

The four-day AI-A02 proof of concept instead requires a
minimal, testable implementation that demonstrates execution
traceability and operational failure handling.

## Decision

Use LangGraph workflow state, in-memory execution history,
and Python standard-library JSON logging.

Record:
- Request correlation ID
- Workflow mode
- Execution duration
- Governance decision
- Final workflow outcome
- Error count and workflow step count

## Alternatives

- PostgreSQL with persistent workflow records
- LangGraph persistence/checkpointing
- OpenTelemetry distributed tracing
- Managed observability platforms

## Rationale

The selected approach introduces no additional infrastructure
or Python dependencies.

It provides sufficient evidence for validating workflow
execution, governance outcomes and basic failure diagnostics.

## Evidence

- Structured workflow events generated successfully
- Successful deterministic execution measured
- Seven observability tests passed
- Full regression suite: 39 tests passed
- Remote A2A success and unavailable-server rejection verified

## Consequences

Workflow state and logs are not a durable audit store.

There is no distributed trace across the orchestrator and
remote A2A service.

## Production Evolution

Introduce persistent checkpointing, durable audit records,
OpenTelemetry instrumentation, and centralized monitoring
when durability, recovery or distributed diagnostics become
operational requirements.
