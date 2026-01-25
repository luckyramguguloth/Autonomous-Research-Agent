from langgraph.graph import StateGraph, END
from .state import AgentState
from .planner import plan_node
from .researcher import researcher_node
from .extractor import extractor_node
from .verifier import verifier_node
from .reporter import reporter_node

def should_continue(state: AgentState):
    """
    Determines if we should continue researching or move to reporting.
    """
    plan = state.get("plan", [])
    current_idx = state.get("tool_calls_count", 0)
    
    if current_idx < len(plan):
        return "researcher"
    return "reporter"

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("planner", plan_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("extractor", extractor_node)
workflow.add_node("verifier", verifier_node)
workflow.add_node("reporter", reporter_node)

# Add Edges
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "extractor")
workflow.add_conditional_edges(
    "extractor",
    should_continue,
    {
        "researcher": "researcher",
        "reporter": "verifier"  # Go to verifier before reporter
    }
)
workflow.add_edge("verifier", "reporter")
workflow.add_edge("reporter", END)

# Compile
app = workflow.compile()
