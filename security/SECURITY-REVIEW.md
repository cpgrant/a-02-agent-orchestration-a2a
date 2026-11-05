# AI-A02 — Software Supply Chain & Security Review

**Assessment date:** 2026-11-05
**Scope:** Four-day agent orchestration and A2A architecture prototype.

## 1. Security evidence

| Control | Evidence | Result |
|---|---|---|
| Python dependency inventory | `sbom-python.cdx.json` | CycloneDX 1.6; 67 components |
| Vulnerability audit | `dependency-audit.json` | 65 dependencies; 0 reported vulnerabilities |
| Dependency consistency | `python -m pip check` | Passed at baseline |
| Runtime inventory | `ai-runtime-inventory.json` | Ollama, models, GPU and driver recorded |
| Workflow regression tests | `python -m pytest -q` | 32 passed |
| Governance | `src/governance/` | PERMIT, DENY, REQUIRE_APPROVAL tested |

## 2. Architecture and governance

The application uses LangGraph orchestration, a separate A2A
agent service, and a deterministic governance policy gate.

Governance outcomes:
- PERMIT: finalize the recommendation.
- DENY: reject the recommendation.
- REQUIRE_APPROVAL: enter a terminal hold state without finalization.

The hold state is a prototype mechanism, not a persistent
human-approval process.

The governance engine currently executes in Python.
Open Policy Agent is a candidate for future independent,
centrally managed policy enforcement.

## 3. AI runtime

- Inference runtime: Ollama 0.40.13
- AI-A02 LLM-backed workflow: Granite 4.2 8B
- GPU: NVIDIA RTX 4090
- NVIDIA driver: 617.42

The runtime inventory includes other installed models.
Their presence does not establish that AI-A02 uses them.

The Python SBOM does not cover Ollama binaries, model weights,
GPU drivers, or operating-system packages.

## 4. Residual risks and limitations

1. The A2A prototype requires further authentication,
   authorization, and transport-security hardening.
2. Persistent workflow checkpointing and human approval
   are not implemented.
3. Dependency scanning detects reported vulnerabilities,
   not unknown vulnerabilities or all configuration issues.
4. Model provenance, licenses, and integrity require
   separate review.
5. Operational logging, tracing, metrics and resilience
   checks remain to be validated.
6. Governance policies are application-local rather than
   centrally distributed.
7. The prototype has not undergone a production security
   assessment or penetration test.

## 5. Assessment conclusion

The Python dependency audit reported no known vulnerabilities
among 65 audited dependencies on 2026-11-05.

The system demonstrates basic governance enforcement,
dependency inventory and repeatable workflow testing.

This is suitable evidence for an architecture proof of concept,
but does not establish production security readiness.

## 6. Recommended production improvements

- Authenticate and authorize A2A clients and tool calls.
- Introduce durable workflow state and human approval.
- Evaluate independent policy enforcement using OPA.
- Adopt structured audit events and distributed tracing.
- Implement automated SBOM generation and vulnerability
  scanning in CI.
- Verify model provenance, licenses and integrity.
- Add security testing and operational resilience checks.
