import pytest
from src.graph.manager import KnowledgeGraphManager
from src.agent.state import AgentState

def test_graph_manager():
    kg = KnowledgeGraphManager()
    kg.add_triplet("Alice", "knows", "Bob")
    assert kg.graph.has_edge("Alice", "Bob")
    assert "known" not in kg.get_summary() # Should verify content
    assert "Alice -> [knows] -> Bob" in kg.get_summary()

def test_agent_state_initialization():
    state = AgentState(
        task="Test Task",
        plan=[],
        current_step="",
        research_results=[],
        graph_triplets=[],
        final_report="",
        tool_calls_count=0
    )
    assert state["task"] == "Test Task"

def test_workflow_import():
    """
    Verifies that the workflow application can be imported without errors.
    This implicitly checks for syntax errors and API key availability (via conftest).
    """
    from src.agent.workflow import app
    assert app is not None
