
# AI-A02 — Operations Runbook

**Project:** Agent Orchestration & A2A
**Scope:** Local architecture proof of concept
**Updated:** 2026-11-05

## 1. Environment

- Operating system: Ubuntu / WSL2
- Python: 3.12.3
- Virtual environment: `.venv`
- Inference runtime: Ollama 0.40.13
- GPU: NVIDIA RTX 4090
- A2A service: `http://127.0.0.1:8001`

## 2. Activate the Project

```bash
cd ~/development/ai-projects/a-02-agent-orchestration-a2a
source .venv/bin/activate
```

Verify:

```bash
which python
python --version
```

## 3. Run the Deterministic Workflow

```bash
python -m scripts.run_workflow --mode deterministic
```

Expected results:

- Research, Analysis and Review execute
- Governance returns PERMIT for the successful example
- A recommendation is finalized
- Structured JSON telemetry is emitted

## 4. Run the LLM-Backed Workflow

Check Ollama and installed models:

```bash
ollama --version
ollama list
```

Run:

```bash
python -m scripts.run_workflow --mode llm
```

The LLM workflow uses the configured local model and requires the Ollama service to be available.

## 5. Start the Independent A2A Server

In a second Ubuntu terminal:

```bash
cd ~/development/ai-projects/a-02-agent-orchestration-a2a
source .venv/bin/activate
python -m src.a2a_server.server
```

Keep this terminal running.

## 6. Verify the A2A Agent Card

In the original terminal:

```bash
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' \
  http://127.0.0.1:8001/.well-known/agent-card.json
```

Expected response:

```text
HTTP 200
```

Inspect the Agent Card:

```bash
curl -s http://127.0.0.1:8001/.well-known/agent-card.json \
  | python -m json.tool
```

Expected characteristics:

- Architecture Assessment Agent
- JSON-RPC protocol binding
- A2A protocol version 1.0
- Architecture assessment skill

## 7. Test Remote A2A Execution

With the server running:

```bash
python -m scripts.a2a_client
```

Expected result:

```text
A2A CLIENT TEST: PASSED
```

The current demonstration client runs its example even when invoked with `--help`.

## 8. Test A2A Failure Handling

Stop the A2A server with Ctrl+C.

Verify it is unavailable:

```bash
curl -sS --max-time 3 -o /dev/null \
  -w 'HTTP %{http_code}\n' \
  http://127.0.0.1:8001/.well-known/agent-card.json
```

Expected: connection refused and HTTP 000.

Run:

```bash
python - <<'PY'
from src.orchestrator.initial_state import create_initial_state
from src.orchestrator.supervisor import build_workflow

result = build_workflow(
    mode="deterministic",
    use_a2a=True,
).invoke(
    create_initial_state("Assess an enterprise multi-agent architecture")
)

assert result["errors"]
assert not result.get("recommended_option")

print("Errors:", result["errors"])
print("Execution trace:", result["execution_log"])
print("A2A FAILURE-HANDLING TEST: PASSED")
PY
```

Expected behavior:

- A remote connection error is recorded
- The workflow routes to rejection
- No recommendation is finalized

## 9. Governance

Implemented policy decisions:

| Decision | Action |
|---|---|
| PERMIT | Finalize recommendation |
| DENY | Reject recommendation |
| REQUIRE_APPROVAL | Enter terminal hold state |

The approval-required state does not currently support durable human approval or resume.

Agent failures encountered before governance evaluation route directly to rejection.

## 10. Observability

The workflow runner produces structured JSON events.

Captured fields include:

- UTC timestamp
- Request ID
- Workflow execution mode
- Execution duration
- Outcome
- Governance decision
- Error count
- Execution step count

The implementation uses Python standard-library logging.

It does not implement OpenTelemetry distributed tracing or durable centralized log storage.

## 11. Automated Testing

Run the entire suite:

```bash
python -m pytest -q
```

Last verified result:

```text
39 passed in 0.23s
```

## 12. Software Supply-Chain Security

Security artifacts:

| File | Purpose |
|---|---|
| `security/python-packages-baseline.txt` | Python dependency snapshot |
| `security/sbom-python.cdx.json` | CycloneDX software bill of materials |
| `security/dependency-audit.json` | pip-audit vulnerability results |
| `security/ai-runtime-inventory.json` | Ollama, models, GPU and driver inventory |
| `security/SECURITY-REVIEW.md` | Security findings and limitations |

Recorded results:

- CycloneDX specification: 1.6
- SBOM components: 67
- Python dependencies audited: 65
- Known vulnerabilities reported: 0

The security tools are installed separately at:

`~/ai-security-tools/`

Repeat the audit:

```bash
~/ai-security-tools/bin/pip-audit \
  -r security/python-packages-baseline.txt \
  --format json \
  --output security/dependency-audit.json
```

Do not automatically upgrade dependencies without compatibility testing.

## 13. Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| HTTP 000 on port 8001 | A2A service stopped | Start the server |
| Uvicorn module import error | Incorrect module path | Use `python -m src.a2a_server.server` |
| Remote assessment rejected | Service or protocol failure | Inspect workflow errors |
| LLM workflow unavailable | Ollama service or model issue | Check Ollama |
| Governance DENY | Rejected review or policy failure | Inspect policy results |
| Approval hold | Approval requested | Manual continuation not implemented |
| Dependency vulnerabilities | Vulnerable version identified | Review advisory and test remediation |

## 14. Operational Limitations

The prototype does not yet include:

- Persistent LangGraph checkpoints
- Durable human approval and resume
- Production authentication and authorization
- Centralized audit storage
- Distributed tracing
- Automatic service recovery
- High-availability deployment

These are documented architectural evolution requirements, not implemented features.

## 15. Shutdown

Stop the A2A server using Ctrl+C.

When finished:

```bash
deactivate
```
