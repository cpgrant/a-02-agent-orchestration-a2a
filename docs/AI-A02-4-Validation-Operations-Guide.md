
# AI-A02-4 — Governance, Validation & Operations
## Day 4 Technical Implementation Guide

**Project:** AI-A02 — Agent Orchestration & A2A
**Date:** 2026-11-05
**Environment:** Ubuntu / WSL2, Python 3.12.3
**Status:** Implementation and operational validation completed; final portfolio closeout pending

---

## 1. Executive Overview

Day 4 extends the agent orchestration and A2A interoperability capabilities developed during Days 1–3.

The primary objective is to demonstrate that a multi-agent architecture can be governed, validated, observed and operated with predictable failure behavior.

Day 4 delivers:

1. Deterministic governance policy enforcement
2. LangGraph governance integration
3. Software Bill of Materials (SBOM)
4. Python dependency vulnerability audit
5. AI runtime inventory
6. Structured workflow observability
7. A2A connectivity and failure-path validation
8. Architecture decision and operational documentation

The implementation is an architecture proof of concept, not a production-ready enterprise deployment.

## 2. Architecture

The implemented execution sequence is:

```text
START
  |
Research Agent
  |
Analysis Agent
  |
[Optional Remote A2A Agent]
  |
Review Agent
  |
Governance Policy Gate
  |
  +-- PERMIT ------------> Finalize
  |
  +-- DENY --------------> Reject
  |
  +-- REQUIRE_APPROVAL --> Hold
                              |
                             END
```

Errors raised by Research, Analysis or the optional Remote A2A Agent route directly to rejection.

These early failure paths do not pass through the governance policy node.

The Hold node represents an approval-required terminal outcome. Persistent approval and workflow resumption are not implemented.

## 3. Governance Policy Engine

### 3.1 Source files

| File | Responsibility |
|---|---|
| `src/governance/policy.py` | Policy decisions and evaluation |
| `src/governance/node.py` | LangGraph governance node, routing and hold behavior |
| `src/orchestrator/state.py` | Governance state fields |
| `src/orchestrator/supervisor.py` | Graph integration and conditional routing |

### 3.2 Decision model

The policy engine returns one of three decisions:

| Decision | Condition | Outcome |
|---|---|---|
| PERMIT | Review approved, no errors, no additional approval required | Finalize |
| DENY | Review rejected or errors present | Reject |
| REQUIRE_APPROVAL | Review approved but explicit approval required | Hold |

The policy also returns a reason and policy identifier.

### 3.3 LangGraph integration

The Review Agent transfers control to the Governance node.

The governance node evaluates the current workflow state and records the policy decision.

Conditional edges select Finalize, Reject or Hold.

### 3.4 Validation

Six unit tests verify policy evaluation.

Three integration tests verify governance behavior inside LangGraph.

All three decisions have been exercised successfully.

### 3.5 Accepted limitation

The current implementation uses application-local Python policies.

OPA is a candidate for independent enterprise policy enforcement but is not implemented in AI-A02.

## 4. Software Supply-Chain Security

### 4.1 Security tooling

Security tools were installed in a separate Python environment:

`~/ai-security-tools/`

Tools:

- CycloneDX Python CLI 8.0.1
- pip-audit 2.10.1

The separate environment avoids modifying AI-A02 application dependencies.

### 4.2 Generate the Python SBOM

```bash
~/ai-security-tools/bin/cyclonedx-py environment \
  .venv/bin/python \
  --output-format JSON \
  --output-file security/sbom-python.cdx.json
```

Verified output:

- Format: CycloneDX
- Specification: 1.6
- Components: 67
- File size: 85,202 bytes

### 4.3 Audit dependency vulnerabilities

```bash
~/ai-security-tools/bin/pip-audit \
  -r security/python-packages-baseline.txt \
  --format json \
  --output security/dependency-audit.json
```

Verified findings:

- Dependencies audited: 65
- Reported known vulnerabilities: 0

This result reflects the packages and vulnerability sources evaluated at the time of the audit.

It does not establish that the complete system is free of security vulnerabilities.

### 4.4 AI runtime inventory

The inventory is stored in:

`security/ai-runtime-inventory.json`

Recorded environment:

| Component | Version or configuration |
|---|---|
| Python | 3.12.3 |
| Ollama | 0.40.13 |
| GPU | NVIDIA RTX 4090 |
| GPU memory | 24,564 MiB |
| NVIDIA driver | 617.42 |

Five locally installed Ollama models were inventoried.

Granite 4.2 8B was used for the AI-A02 LLM-backed implementation.

Installed models must not be confused with models actually exercised in project tests.

### 4.5 Security limitations

The Python SBOM does not comprehensively cover:

- Operating-system packages
- Ollama binaries
- Model weights and provenance
- NVIDIA driver vulnerabilities
- Deployment configuration security

The security assessment is documented in:

`security/SECURITY-REVIEW.md`

## 5. Structured Observability

### 5.1 Implementation files

- `src/observability/workflow.py`
- `scripts/run_workflow.py`

The implementation uses the Python standard library.

### 5.2 Recorded telemetry

The observed workflow wrapper records:

- UTC timestamp
- Request identifier
- Execution mode
- Execution duration in milliseconds
- Final outcome
- Governance decision
- Error count
- Execution-log step count

### 5.3 Outcomes

| Outcome | Interpretation |
|---|---|
| COMPLETED | Approved and finalized |
| REJECTED | Rejected or failed |
| AWAITING_APPROVAL | Approval required |
| UNKNOWN | Unclassified terminal state |
| FAILED | Workflow invocation raised an exception |

### 5.4 Execute the observed workflow

```bash
python -m scripts.run_workflow --mode deterministic
```

A successful execution produced:

- Outcome: COMPLETED
- Governance: PERMIT
- Errors: 0
- Steps: 5
- Duration: 3.17 ms

The recorded execution time is a single deterministic observation, not a throughput or latency benchmark.

### 5.5 Test coverage

Seven observability unit tests passed, including outcome classification, telemetry generation and exception logging.

## 6. A2A Operational Verification

### 6.1 Start the service

In a separate terminal:

```bash
cd ~/development/ai-projects/a-02-agent-orchestration-a2a
source .venv/bin/activate
python -m src.a2a_server.server
```

### 6.2 Agent discovery

```bash
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' \
  http://127.0.0.1:8001/.well-known/agent-card.json
```

Verified result: HTTP 200.

The Agent Card advertised:

- Architecture Assessment Agent
- Agent version 1.0.0
- JSON-RPC protocol binding
- Protocol version 1.0
- Architecture assessment skill

### 6.3 Remote task execution

```bash
python -m scripts.a2a_client
```

Verified result:

`A2A CLIENT TEST: PASSED`

The remote service returned a structured architecture assessment, strengths, risks and recommendation.

### 6.4 Failure-path verification

The server was stopped and its unavailability verified using curl.

Observed response: connection refused, HTTP 000.

The workflow was then executed with remote A2A enabled.

Recorded behavior:

1. Research completed.
2. Analysis completed.
3. Remote A2A assessment failed.
4. Connection error was recorded.
5. Supervisor routed to rejection.
6. No recommendation was finalized.

Verified result:

`A2A FAILURE-HANDLING TEST: PASSED`

This demonstrates fail-closed behavior for the tested remote-service outage scenario.

It does not establish resilience against every possible network or protocol failure.

## 7. Automated Regression Testing

Run:

```bash
python -m pytest -q
```

Latest verified result:

`39 passed in 0.23s`

Relevant Day 4 test files:

| File | Validation |
|---|---|
| `tests/unit/test_governance.py` | Policy decisions |
| `tests/integration/test_governance_workflow.py` | LangGraph governance routing |
| `tests/unit/test_observability.py` | Operational telemetry and exception behavior |

Existing Day 1–3 tests remain part of the full regression suite.

## 8. Architecture Decision Review

Six ADRs are recorded.

- ADR-001: LangGraph Orchestration
- ADR-002: Supervisor-Worker Architecture
- ADR-003: A2A Interoperability
- ADR-004: Original Persistence and Tracing Decision — Superseded
- ADR-005: Implemented State and Observability
- ADR-006: Governance Policy Enforcement

ADR-004 originally selected PostgreSQL and OpenTelemetry.

The implemented proof of concept instead uses in-memory state and structured JSON logs.

ADR-005 formally records this change.

The architectural rationale, alternatives, accepted risks and production evolution plan are documented in:

`docs/AI-A02-Architecture-Decision-Review.md`

## 9. Operational Procedures

See:

`docs/AI-A02-Operations-Runbook.md`

The runbook covers:

- Environment activation
- Deterministic and LLM execution
- A2A service startup and verification
- Remote-agent testing
- Failure simulation
- Governance behavior
- Security tooling
- Troubleshooting
- Shutdown

## 10. Known Limitations

AI-A02 does not implement:

- Persistent LangGraph checkpointing
- Durable human approval and resume
- Production authentication and authorization
- Independent OPA policy enforcement
- Centralized logging and audit retention
- OpenTelemetry distributed tracing
- Automatic A2A recovery
- High-availability deployment

These limitations should be addressed according to actual production requirements and risk assessments.

## 11. Day 4 Deliverables

| Deliverable | Status |
|---|---|
| Python governance engine | Completed |
| LangGraph governance integration | Completed |
| Governance tests | Completed |
| CycloneDX SBOM | Completed |
| Dependency vulnerability audit | Completed |
| AI runtime inventory | Completed |
| Security review | Completed |
| Structured observability | Completed |
| Observability tests | Completed |
| A2A connectivity and failure validation | Completed |
| Architecture Decision Review | Draft created |
| Operations Runbook | Created |
| Day 4 Technical Guide | Prepared for final review |

## 12. Project Closeout

Remaining project-wide activities:

1. Final architecture diagrams and verification
2. Consolidated Days 1–4 project report
3. README update
4. Final regression and documentation review
5. Git commit and GitHub push

## 13. Conclusion

Day 4 demonstrates that the AI-A02 architecture supports deterministic governance, software inventory, basic operational observability and controlled failure handling.

The complete project combines architecture design, working orchestration, independent A2A interoperability and validation evidence.

Its principal value is a reproducible and critically evaluated enterprise AI architecture proof of concept.
