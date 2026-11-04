"""Export the implemented AI-A02 LangGraph topology."""

from pathlib import Path

from src.orchestrator.supervisor import build_workflow


def main():
    output_dir = Path("diagrams/rendered")
    output_dir.mkdir(parents=True, exist_ok=True)

    workflow = build_workflow(mode="deterministic")
    graph = workflow.get_graph()

    mermaid_source = graph.draw_mermaid()

    source_path = Path("diagrams/05-implemented-langgraph.mmd")
    source_path.write_text(mermaid_source, encoding="utf-8")

    print("Mermaid source:", source_path)
    print("Graph nodes:", list(graph.nodes))
    print("Graph edges:", len(graph.edges))


if __name__ == "__main__":
    main()
