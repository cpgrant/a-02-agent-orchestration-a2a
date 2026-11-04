"""Integration-boundary tests for the A2A 1.0 client."""

import json
from unittest.mock import patch

import pytest

from scripts.a2a_client import assess_remotely


ASSESSMENT = {
    "request": "Evaluate an enterprise multi-agent architecture",
    "assessment": "Preliminary architecture assessment",
    "strengths": ["Independent agent deployment"],
    "risks": ["Network failure"],
    "recommendation": "Validate remote execution.",
}


class FakeHTTPResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, *args):
        return self.payload


def completed_response(artifacts=None):
    if artifacts is None:
        artifacts = [
            {
                "name": "architecture-assessment",
                "parts": [
                    {
                        "text": json.dumps(ASSESSMENT),
                        "mediaType": "application/json",
                    }
                ],
            }
        ]

    return {
        "jsonrpc": "2.0",
        "id": "test-request",
        "result": {
            "task": {
                "status": {"state": "TASK_STATE_COMPLETED"},
                "artifacts": artifacts,
            }
        },
    }


def test_successful_a2a_assessment():
    with patch(
        "urllib.request.urlopen",
        return_value=FakeHTTPResponse(completed_response()),
    ) as mock_urlopen:
        result = assess_remotely("Evaluate architecture")

    assert result == ASSESSMENT

    request = mock_urlopen.call_args.args[0]
    assert request.get_header("A2a-version") == "1.0"
    assert request.get_method() == "POST"


def test_empty_request_rejected():
    with pytest.raises(ValueError):
        assess_remotely("   ")


def test_a2a_protocol_error():
    response = {
        "jsonrpc": "2.0",
        "id": "test-request",
        "error": {
            "code": -32009,
            "message": "Unsupported A2A version",
        },
    }

    with patch(
        "urllib.request.urlopen",
        return_value=FakeHTTPResponse(response),
    ):
        with pytest.raises(RuntimeError, match="A2A error"):
            assess_remotely("Evaluate architecture")


def test_incomplete_remote_task():
    response = completed_response()
    response["result"]["task"]["status"]["state"] = "TASK_STATE_WORKING"

    with patch(
        "urllib.request.urlopen",
        return_value=FakeHTTPResponse(response),
    ):
        with pytest.raises(RuntimeError, match="not completed"):
            assess_remotely("Evaluate architecture")


def test_missing_assessment_artifact():
    with patch(
        "urllib.request.urlopen",
        return_value=FakeHTTPResponse(completed_response(artifacts=[])),
    ):
        with pytest.raises(RuntimeError, match="No architecture assessment"):
            assess_remotely("Evaluate architecture")
