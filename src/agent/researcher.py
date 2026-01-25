from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..tools import web_search, scrape_content
from .state import AgentState



def researcher_node(state: AgentState):
    """
    Executes the next step in the research plan.
    """
    plan = state["plan"]
    current_step_idx = state.get("tool_calls_count", 0)
    
    if current_step_idx >= len(plan):
        return {"research_results": ["Research complete."]}
        
    current_step = plan[current_step_idx]
    
    # Decide whether to search or just answer (simple router)
    # For now, we assume every step requires search
    search_results = web_search.invoke({"query": current_step})
    
    # Optionally scrape the first result if it looks promising (simplification)
    # In a real system, we'd parse the search results and pick URLs.
    
    return {
        "research_results": [f"Step: {current_step}\nResults: {search_results}"],
        "current_step": current_step,
        "tool_calls_count": current_step_idx + 1
    }
