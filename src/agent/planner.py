from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import AgentState
import os

# Removed global LLM init

PLANNER_PROMPT = """
You are a highly precise research planner for an autonomous agent.
Your goal is to create a structured, step-by-step research plan for the query: {task}

Requirements:
1. Break the topic into 2-3 distinct, high-impact search steps.
2. Focus ONLY on gathering factual, verifiable data (statistics, official reports, credible news).
3. Avoid vague steps. Be specific: "Search for X market size in 2025/2026".
4. ALWAYS include the current year (2025/2026) in search queries to get up-to-date info.
4. If the query asks for future prediction/opinion, plan to search for *expert analyses* rather than generating your own.

Return ONLY a numbered list of steps. Do not include introductory text.
"""

def plan_node(state: AgentState):
    """
    Generates a research plan for the given task.
    """
    task = state["task"]
    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
    model_name = state.get("model_name", "gemini-3-flash-preview")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    chain = prompt | llm | StrOutputParser()
    
    plan_text = chain.invoke({"task": task})
    
    # Simple parsing of the numbered list
    steps = [line.strip().lstrip("1234567890. ") for line in plan_text.split("\n") if line.strip()]
    
    return {"plan": steps}
