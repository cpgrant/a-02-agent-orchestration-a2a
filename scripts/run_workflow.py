"""Execute AI-A02 in deterministic or LLM mode."""

import argparse

from src.orchestrator.initial_state import create_initial_state
from src.orchestrator.supervisor import build_workflow


def main():
    parser = argparse.ArgumentParser(
        description="AI-A02 Multi-Agent Orchestration"
    )

    parser.add_argument(
        "--mode",
        choices=["deterministic", "llm"],
        default="deterministic",
    )

    parser.add_argument(
        "--request",
        default="Evaluate local LLM versus managed cloud AI",
    )

    args = parser.parse_args()

    workflow = build_workflow(mode=args.mode)
    state = create_initial_state(args.request)

    result = workflow.invoke(state)

    print("\nAI-A02 — Multi-Agent Workflow")
    print("=" * 50)
    print("Mode:", args.mode)
    print("Request ID:", result["request_id"])
    print("Research findings:", len(result["research_findings"]))
    print("Architecture options:", len(result["architecture_options"]))
    print("Review approved:", result["review_approved"])
    print("Recommendation:", result["recommended_option"])
    print("Rationale:", result["recommendation_rationale"])

    print("\nExecution trace:")
    for event in result["execution_log"]:
        print("-", event)

    print("\nErrors:", result["errors"])


if __name__ == "__main__":
    main()
