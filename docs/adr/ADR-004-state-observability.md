# ADR-004 — State and Observability

Status: Superseded by ADR-005

## Context
Multi-agent execution requires task traceability,
persistent records and failure diagnostics.

## Decision
Use PostgreSQL for persistent task and execution
records and OpenTelemetry for distributed tracing.

## Alternatives
- In-memory state only
- SQLite for persistent records
- Application logging without tracing

## Rationale
These technologies align with the AI-A01 platform
and support observable, reproducible workflows.

## Consequences
Database persistence and tracing must be integrated
and validated without excessive infrastructure.
