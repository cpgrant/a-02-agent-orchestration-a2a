"""LLM-backed architecture Analysis Agent."""

from src.contracts.models import ArchitectureAssessment
from src.llm.client import generate_structured
from src.orchestrator.state import WorkflowState


def analysis_llm_agent(state: WorkflowState) -> dict:
    """Generate structured assessments using Ollama."""

    if not state["research_findings"]:
        return {
            "errors": state["errors"] + [
                "Analysis LLM Agent: research findings missing"
            ],
            "execution_log": state["execution_log"] + [
                "Analysis LLM Agent: failed"
            ],
        }

    assessments = []

    try:
        research_context = "\n".join(
            f"- {finding}"
            for finding in state["research_findings"]
        )

        for option in ("Local LLM", "Managed Cloud AI"):
            assessment = generate_structured(
                system_prompt=(
                    "You are an enterprise AI architecture analyst. "
                    "Assess only the specified architecture option. "
                    "Return structured, technically grounded results. "
                    "Do not invent financial measurements."
                ),
                user_prompt=(
                    f"Architecture request: {state['request']}\n"
                    f"Option to assess: {option}\n"
                    f"Set the option field exactly to '{option}'.\n"
                    f"Research findings:\n{research_context}\n"
                    "Provide advantages, disadvantages, "
                    "operational risks, governance considerations, "
                    "and a qualitative cost assessment."
                ),
                schema=ArchitectureAssessment,
            )

            # Verify semantic correctness, not just JSON structure.
            if assessment.option != option:
                raise ValueError(
                    f"Expected option '{option}', "
                    f"received '{assessment.option}'"
                )

            assessments.append(assessment.model_dump())

        return {
            "architecture_options": assessments,
            "execution_log": state["execution_log"] + [
                "Analysis LLM Agent: completed"
            ],
        }

    except Exception as exc:
        return {
            "errors": state["errors"] + [
                f"Analysis LLM Agent failed: {type(exc).__name__}"
            ],
            "execution_log": state["execution_log"] + [
                "Analysis LLM Agent: failed"
            ],
        }
