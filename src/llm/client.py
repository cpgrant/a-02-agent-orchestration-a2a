"""Ollama client for AI-A02 local model inference."""

import os

import httpx


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "granite4.2:8b",
)


def generate(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
) -> str:
    """Generate a response using a local Ollama model."""

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "think": False,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 1024,
        },
    }

    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
        )
        response.raise_for_status()

    result = response.json()

    if result.get("done_reason") == "length":
        raise RuntimeError("LLM output truncated")

    content = result.get("message", {}).get("content", "")

    if not content.strip():
        raise RuntimeError("LLM returned empty content")

    return content


def generate_structured(
    system_prompt: str,
    user_prompt: str,
    schema: type,
    model: str | None = None,
):
    """Generate and validate a Pydantic-compatible JSON response."""

    from pydantic import BaseModel

    if not issubclass(schema, BaseModel):
        raise TypeError("schema must be a Pydantic BaseModel")

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    system_prompt
                    + "\nReturn only JSON matching the supplied schema."
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
        "format": schema.model_json_schema(),
        "think": False,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 2048,
        },
    }

    with httpx.Client(timeout=180.0) as client:
        response = client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
        )
        response.raise_for_status()

    result = response.json()

    if result.get("done_reason") == "length":
        raise RuntimeError("Structured LLM output truncated")

    content = result.get("message", {}).get("content", "")

    if not content.strip():
        raise RuntimeError("Structured LLM output is empty")

    return schema.model_validate_json(content)
