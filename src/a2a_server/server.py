"""Independent A2A Architecture Assessment server."""

import uvicorn

from starlette.applications import Starlette

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentInterface,
    AgentSkill,
)

from src.a2a_server.executor import ArchitectureAssessmentExecutor


HOST = "127.0.0.1"
PORT = 8001
URL = f"http://{HOST}:{PORT}/"


def build_agent_card() -> AgentCard:
    return AgentCard(
        name="AI-A02 Architecture Assessment Agent",
        description=(
            "Independent A2A agent providing preliminary "
            "enterprise architecture assessments."
        ),
        version="1.0.0",
        supported_interfaces=[
            AgentInterface(
                url=URL,
                protocol_binding="JSONRPC",
                protocol_version="1.0",
            )
        ],
        capabilities=AgentCapabilities(
            streaming=False,
            push_notifications=False,
        ),
        default_input_modes=["text/plain"],
        default_output_modes=["application/json"],
        skills=[
            AgentSkill(
                id="architecture_assessment",
                name="Architecture Assessment",
                description=(
                    "Evaluate enterprise architecture requests "
                    "and return structured findings."
                ),
                tags=[
                    "architecture",
                    "enterprise-ai",
                    "assessment",
                ],
                examples=[
                    "Evaluate an enterprise multi-agent architecture"
                ],
                input_modes=["text/plain"],
                output_modes=["application/json"],
            )
        ],
    )


def build_app() -> Starlette:
    card = build_agent_card()

    handler = DefaultRequestHandler(
        agent_executor=ArchitectureAssessmentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )

    return Starlette(
        routes=[
            *create_agent_card_routes(card),
            *create_jsonrpc_routes(handler, "/"),
        ]
    )


app = build_app()


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
