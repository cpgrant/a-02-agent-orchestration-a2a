"""AI-A02: A2A Protocol 1.0 architecture assessment client."""

import json
import uuid
import urllib.error
import urllib.request


A2A_URL = "http://127.0.0.1:8001/"


def assess_remotely(
    request_text: str,
    url: str = A2A_URL,
) -> dict:
    """Submit an A2A request and return its assessment artifact."""

    if not request_text.strip():
        raise ValueError("Request must not be empty")

    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "SendMessage",
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "ROLE_USER",
                "parts": [{"text": request_text}],
            }
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "A2A-Version": "1.0",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    if "error" in data:
        raise RuntimeError(f"A2A error: {data['error']}")

    task = data["result"]["task"]

    if task["status"]["state"] != "TASK_STATE_COMPLETED":
        raise RuntimeError(
            f"A2A task not completed: {task['status']['state']}"
        )

    artifacts = task.get("artifacts", [])

    for artifact in artifacts:
        if artifact.get("name") == "architecture-assessment":
            for part in artifact.get("parts", []):
                if "text" in part:
                    return json.loads(part["text"])

    raise RuntimeError("No architecture assessment artifact returned")


if __name__ == "__main__":
    result = assess_remotely(
        "Evaluate an enterprise multi-agent architecture"
    )

    print("\nAI-A02 Remote A2A Assessment")
    print("=" * 40)
    print(json.dumps(result, indent=2))
    print("\nA2A CLIENT TEST: PASSED")
