# ADR-002 — Supervisor-Worker Architecture

Status: Accepted

## Context
Agent responsibilities and delegation authority must
be explicit and observable.

## Decision
Use one supervisor coordinating three local specialist
agents: Research, Analysis and Review.

## Alternatives
- Decentralized peer-to-peer collaboration
- Sequential single-agent execution

## Rationale
Centralized orchestration simplifies authorization,
coordination, testing and execution tracing.

## Consequences
The supervisor is a coordination dependency.
Failure handling and recovery must be tested.
