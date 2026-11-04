# ADR-003 — A2A Interoperability

Status: Accepted

## Context
AI-A02 must demonstrate collaboration with an
independently deployed agent.

## Decision
Use the A2A protocol across the remote agent boundary.
Use native LangGraph calls for local specialist agents.

## Alternatives
- Direct REST API calls
- Shared Python library calls
- Framework-specific remote execution

## Rationale
A2A provides standardized agent discovery and
task-oriented interoperability.

## Consequences
The project requires an independent A2A service,
agent metadata and protocol-level tests.

The implementation must verify SDK compatibility
with the selected A2A protocol version.
