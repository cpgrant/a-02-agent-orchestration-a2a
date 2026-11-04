# ADR-001 — LangGraph Orchestration

Status: Accepted

## Context
AI-A02 requires controlled multi-agent workflows with
explicit routing, state transitions and failure handling.

## Decision
Use LangGraph as the local orchestration framework.

## Alternatives
- CrewAI
- AutoGen
- Custom Python orchestration

## Rationale
LangGraph supports explicit stateful workflows,
conditional routing and controlled execution.

## Consequences
The local agent workflow depends on LangGraph.
External interoperability remains separate through A2A.
