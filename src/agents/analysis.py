"""Deterministic Analysis Agent for AI-A02."""

from src.contracts.models import ArchitectureAssessment
from src.orchestrator.state import WorkflowState


def analysis_agent(state: WorkflowState) -> dict:
    """Compare architecture alternatives using research findings."""

    if not state["research_findings"]:
        return {
            "errors": state["errors"] + [
                "Analysis Agent: research findings missing"
            ],
            "execution_log": state["execution_log"] + [
                "Analysis Agent: failed"
            ],
        }

    assessments = [
        ArchitectureAssessment(
            option="Local LLM",
            advantages=[
                "Direct control over model hosting",
                "Greater infrastructure customization",
            ],
            disadvantages=[
                "Requires GPU infrastructure",
                "Internal model operations and maintenance",
            ],
            estimated_cost="Requires workload-specific TCO analysis",
            operational_risks=[
                "GPU capacity constraints",
                "Model maintenance overhead",
            ],
            governance_considerations=[
                "Internal access control",
                "Data security and auditability",
            ],
        ),
        ArchitectureAssessment(
            option="Managed Cloud AI",
            advantages=[
                "Reduced model hosting responsibilities",
                "Access to managed infrastructure",
            ],
            disadvantages=[
                "Provider dependency",
                "Usage-based operating costs",
            ],
            estimated_cost="Requires workload-specific pricing analysis",
            operational_risks=[
                "Service availability dependency",
                "Pricing and API changes",
            ],
            governance_considerations=[
                "Data processing agreements",
                "Provider security and compliance review",
            ],
        ),
    ]

    return {
        "architecture_options": [
            assessment.model_dump()
            for assessment in assessments
        ],
        "execution_log": state["execution_log"] + [
            "Analysis Agent: completed architecture comparison"
        ],
    }
