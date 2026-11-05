# ADR-006 — Governance Policy Enforcement

Status: Accepted
Date: 2026-11-05

## Context

AI-A02 requires deterministic governance over multi-agent
workflow outcomes, including review rejection, approval
requirements and permission to finalize.

## Decision

Implement an in-process Python policy engine integrated
with LangGraph.

Supported decisions:
- PERMIT
- DENY
- REQUIRE_APPROVAL

Governance is evaluated after Review when the workflow
reaches that stage.

Earlier agent failures route directly to rejection.

## Alternatives

- Open Policy Agent (OPA) with Rego policies
- Independent custom policy service
- Governance logic embedded in individual agents
- Manual review without executable policy controls

## Rationale

The Python policy engine is simple, deterministic,
independently unit-testable and requires no additional
policy infrastructure.

OPA offers stronger policy/application separation and
reuse across independent enterprise systems, but adds
deployment and operational complexity.

## Evidence

- Policy engine implemented in src/governance/
- Six governance unit tests passed
- Three LangGraph governance integration tests passed
- PERMIT, DENY and REQUIRE_APPROVAL paths verified

## Accepted Limitations

- Policies are deployed with the application
- No centralized policy distribution
- No independent policy administration
- Human approval is represented by a terminal hold state
- No durable approval/resume workflow

## Production Evolution

Consider OPA as an independent Policy Decision Point
when governance policies must be shared across agents,
applications and enterprise services.

Implement authentication, authorization, persistent
approval workflows and durable audit records separately.
