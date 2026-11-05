# AI-A02 — Architecture Decision Review

**Project:** Agent Orchestration & A2A
**Date:** 2026-11-05
**Scope:** Four-day enterprise AI architecture proof of concept

## 1. Executive Assessment

AI-A02 demonstrates controlled multi-agent orchestration,
independent agent interoperability, deterministic governance,
structured observability and operational failure handling.

The architecture prioritizes explicit control flow, modularity,
interoperability, testability and manageable prototype scope.

The implementation is an architecture proof of concept,
not a production-ready autonomous enterprise platform.

## 2. Architecture Evaluation Criteria

| Criterion | Weight |
|---|---:|
| Architectural suitability | 25% |
| Security and governance | 20% |
| Reliability and resilience | 15% |
| Interoperability | 15% |
| Operational complexity | 10% |
| Performance and scalability | 10% |
| Cost and portability | 5% |
| **Total** | **100%** |

These are proposed decision weights, not empirically
derived measurements.

Mandatory requirements, particularly authorization and
security, cannot be overridden by a high weighted score.

No quantitative framework comparison was undertaken.
The following judgments are qualitative and evidence-based.

## 3. Decision Summary

| Area | Selected approach | Main alternatives |
|---|---|---|
| Orchestration | LangGraph | CrewAI, AutoGen, custom Python |
| Agent topology | Supervisor-worker | Peer-to-peer, single agent |
| Interoperability | A2A 1.0 | Custom REST, framework-specific RPC |
| Inference | Local Ollama | Managed APIs, vLLM |
| Execution modes | Deterministic and LLM-backed | LLM-only |
| Governance | Python policy engine | OPA, custom policy service |
| State | In-memory LangGraph state | Persistent checkpointing |
| Observability | JSON operational events | OpenTelemetry |
| Security inventory | CycloneDX | SPDX, alternative SBOM tools |
| Vulnerability audit | pip-audit | Other dependency scanners |

## 4. Architectural Decisions

### 4.1 LangGraph Orchestration — ADR-001

**Decision:** Use LangGraph for local agent execution.

**Rationale:** Explicit state transitions, conditional routing,
agent composition and predictable execution are central to
a controlled multi-agent architecture.

**Trade-off:** LangGraph introduces framework dependency
and does not independently solve enterprise persistence,
security or policy administration.

**Evidence:** Research, Analysis, Review, Governance and
terminal routing were implemented and tested.

**Reconsider when:** The workload requires a different
execution paradigm, simpler orchestration or capabilities
better supported by another framework.

### 4.2 Supervisor-Worker Architecture — ADR-002

**Decision:** Central orchestration of specialist agents.

**Rationale:** Clear responsibility boundaries and centralized
routing simplify governance, debugging and test coverage.

**Trade-off:** The supervisor becomes a coordination
dependency and potential operational bottleneck.

**Evidence:** Local specialist workflow and remote
agent integration demonstrated.

**Reconsider when:** Large-scale independent collaboration
or decentralized execution provides measurable benefits.

### 4.3 A2A Interoperability — ADR-003

**Decision:** Use A2A for an independently deployed
architecture-assessment agent.

**Rationale:** Standardized agent metadata, task-oriented
interaction and protocol boundaries provide stronger
agent interoperability than direct framework coupling.

**Trade-off:** Introduces network dependencies, protocol
compatibility requirements and additional security work.

**Evidence:** Agent Card discovery, successful remote
assessment and unavailable-server rejection demonstrated.

**Reconsider when:** A simple application API is sufficient,
or asynchronous messaging and durable queues better meet
reliability requirements.

A2A is not a replacement for every REST API or MCP tool
integration; those serve different architectural purposes.

### 4.4 Local Inference with Ollama

**Decision:** Support local LLM inference alongside
deterministic agent implementations.

**Rationale:** Supports experimentation with local models
and keeps deterministic test paths independent of model
availability and nondeterministic output.

**Trade-off:** Local inference introduces hardware
constraints, model management and variable execution quality.

**Evidence:** AI-A02 has used Granite 4.2 8B with Ollama;
runtime inventory captured Ollama 0.40.13 and RTX 4090.

**Not established:** Comparative quality, throughput, cost
or latency superiority over managed LLM services.

**Reconsider when:** Workloads demand managed scaling,
specific quality levels or alternative inference engines.

### 4.5 State and Observability — ADR-004/005

**Original decision:** PostgreSQL and OpenTelemetry.

**Implemented decision:** In-memory workflow state,
execution history and standard-library JSON logging.

**Rationale:** Sufficient operational evidence for a
four-day proof of concept without additional infrastructure.

**Evidence:** Request IDs, timing, outcomes, errors and
governance decisions logged; seven observability tests passed.

**Trade-off:** No durable audit store, workflow recovery
or distributed tracing across the A2A boundary.

**Reconsider when:** Restart recovery, durable approvals,
audit retention or distributed diagnostics are required.

ADR-004 remains in the repository as superseded history.

### 4.6 Governance — ADR-006

**Decision:** Implement deterministic Python policy
evaluation within LangGraph.

**Rationale:** Simple, independently testable governance
with explicit PERMIT, DENY and REQUIRE_APPROVAL outcomes.

**Alternative:** Open Policy Agent offers stronger policy
separation and potential reuse across enterprise services.

**Trade-off:** Application-local policies lack independent
policy administration and centralized distribution.

**Evidence:** Six policy unit tests and three governance
integration tests passed.

**Important limitation:** REQUIRE_APPROVAL ends in a hold
state. There is no durable human approval/resume mechanism.

**Reconsider when:** Multiple independently deployed
services need common, centrally governed policies.

## 5. Security and Supply Chain

The project generated:

- CycloneDX 1.6 Python SBOM: 67 components
- pip-audit results: 65 dependencies examined
- Reported known vulnerabilities: zero
- AI runtime inventory and security review

The Python audit does not cover all operating-system
packages, Ollama model weights or NVIDIA driver security.

Zero known vulnerability findings does not establish
overall system security.

Production deployment requires authentication,
authorization, transport security, model provenance,
logging controls and further security validation.

## 6. Operational Validation

Evidence as of 2026-11-05:

- 39 automated regression tests passed
- Three governance outcomes verified
- Structured workflow telemetry demonstrated
- A2A Agent Card retrieved successfully
- Remote A2A task execution succeeded
- Remote outage produced a recorded error
- Failed remote assessment prevented finalization

The observed deterministic workflow duration of 3.17 ms
is one local execution, not a benchmark.

## 7. Accepted Architectural Risks

| Risk | Prototype handling | Production direction |
|---|---|---|
| Remote A2A outage | Reject without finalizing | Timeouts, retries, circuit breaking |
| Missing durable state | In-memory execution | Persistent checkpoints |
| Human approval | Terminal hold | Durable approval/resume |
| Policy fragmentation | Local Python rules | Evaluate OPA |
| Distributed diagnostics | JSON event summaries | OpenTelemetry |
| Unauthorized remote access | Not production hardened | AuthN/AuthZ and TLS |
| Model quality variation | Deterministic test path | Model evaluation suite |
| Dependency vulnerabilities | SBOM and audit | Continuous CI scanning |

## 8. Production Evolution Roadmap

**Stage 1 — Validated proof of concept**

LangGraph, A2A, governance, deterministic testing,
structured logs and dependency security inventory.

**Stage 2 — Operational hardening**

Authentication, authorization, persistent state,
approval/resume, secrets management, structured audit
retention, timeouts and recovery testing.

**Stage 3 — Enterprise integration**

Shared policy enforcement where justified,
enterprise application integration, distributed tracing,
central monitoring and automated security controls.

**Stage 4 — Scaled autonomous operations**

Evaluate workload-specific scalability, agent quality,
cost, resilience and compliance before increasing
autonomous decision authority.

## 9. Final Architectural Judgment

The selected architecture is appropriate for a controlled,
four-day multi-agent interoperability proof of concept.

Its primary strengths are explicit orchestration,
separation of local and remote agents, deterministic
governance and demonstrated failure handling.

Its primary limitations are missing durable execution
state, incomplete enterprise security controls and
limited operational instrumentation.

A production architecture should evolve according to
measured requirements rather than introducing every
enterprise component into the initial prototype.

## 10. Related Records

- ADR-001 — LangGraph Orchestration
- ADR-002 — Supervisor-Worker Architecture
- ADR-003 — A2A Interoperability
- ADR-004 — Original Persistence and Tracing Decision
- ADR-005 — Implemented State and Observability
- ADR-006 — Governance Policy Enforcement
- security/SECURITY-REVIEW.md
