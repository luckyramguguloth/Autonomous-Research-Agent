from typing import TypedDict, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    task: str
    plan: List[str]
    current_step: str
    research_results: Annotated[List[str], operator.add]
    graph_triplets: Annotated[List[Dict[str, str]], operator.add]
    final_report: str
    tool_calls_count: int
    model_name: str
