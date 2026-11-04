from src.agents.research import research_agent
from src.orchestrator.initial_state import create_initial_state


def test_research_agent_returns_findings():
    state = create_initial_state(
        "Evaluate local LLM versus managed cloud AI"
    )

    result = research_agent(state)

    assert len(result["research_findings"]) == 4
    assert all(result["research_findings"])


def test_research_agent_updates_execution_log():
    state = create_initial_state("Architecture assessment")

    result = research_agent(state)

    assert "Research Agent" in result["execution_log"][-1]


def test_research_agent_does_not_mutate_input():
    state = create_initial_state("Architecture assessment")

    research_agent(state)

    assert state["research_findings"] == []
    assert state["execution_log"] == []
