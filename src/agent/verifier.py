from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import AgentState



VERIFY_PROMPT = """
You are a rigorous Fact-Checking Agent.
Your job is to validate the research findings for credibility and accuracy.

Research Log:
{research_results}

Tasks:
1. AGGRESSIVELY check against the Research Log. If a fact is not in the log, it is a HALLUCINATION. Flag it.
2. Assign a credibility score (0-10). If the score is < 7, warn the user.
3. Identify contradictions. If Source A says X and Source B says Y, report the conflict.
4. Output a verification summary explicitly stating what is confirmed vs unconfirmed.

Return the verification report as a markdown string.
"""

def verifier_node(state: AgentState):
    """
    Verifies the collected information.
    """
    prompt = ChatPromptTemplate.from_template(VERIFY_PROMPT)
    model_name = state.get("model_name", "gemini-3-flash-preview")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    chain = prompt | llm | StrOutputParser()
    
    # Check the last few results
    results = state.get("research_results", [])
    if not results:
        return {}
        
    verification = chain.invoke({"research_results": "\n".join(results[-3:])})
    
    # We just append this to the results for the reporter to see
    return {"research_results": [f"--- VERIFICATION REPORT ---\n{verification}"]}
