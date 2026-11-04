"""LLM-backed Research Agent."""

from src.llm.client import generate_structured
from src.llm.schemas import ResearchFindings
from src.orchestrator.state import WorkflowState


def research_llm_agent(state: WorkflowState) -> dict:
    """Generate structured research findings using Ollama."""

    try:
        research = generate_structured(
            system_prompt=(
                "You are an enterprise AI research specialist. "
                "Identify technical considerations for AI architecture. "
                "Distinguish general knowledge from verified evidence. "
                "Do not invent measurements, benchmarks, or sources."
            ),
            user_prompt=(
                f"Architecture request: {state['request']}\n"
                "Provide 3 to 6 concise technical findings. "
                "Identify relevant assumptions and information gaps."
            ),
            schema=ResearchFindings,
        )

        return {
            "research_findings": research.findings,
            "execution_log": state["execution_log"] + [
                "Research LLM Agent: completed"
            ],
        }

    except Exception as exc:
        return {
            "errors": state["errors"] + [
                f"Research LLM Agent failed: {type(exc).__name__}"
            ],
            "execution_log": state["execution_log"] + [
                "Research LLM Agent: failed"
            ],
        }
