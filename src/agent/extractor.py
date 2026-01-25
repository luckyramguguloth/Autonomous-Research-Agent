from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .state import AgentState
from typing import List, Dict



EXTRACTOR_PROMPT = """
You are a strict knowledge graph builder.
Analyze the provided text and extract verifiable entities and relationships.

Text:
{text}

Rules:
1. Extract ONLY the top 3 most important factual triplets.
2. Skip opinions, speculation, or vague statements.
3. Ensure entities are canonical (e.g., use "Google" instead of "the company").
4. Predicates should be lower-case verbs (e.g., "acquired_by", "released_in").
5. DO NOT INFER relationships. If "A is B" is not written, do not extract it.
6. If the text contains no factual assertions, return an empty list.

Return ONLY a valid JSON list of objects with keys: "subject", "predicate", "object".
"""

def extractor_node(state: AgentState):
    """
    Extracts triplets from the latest research results and returns them.
    """
    results = state["research_results"]
    if not results:
        return {}
        
    latest_result = results[-1]
    
    prompt = ChatPromptTemplate.from_template(EXTRACTOR_PROMPT)
    model_name = state.get("model_name", "gemini-3-flash-preview")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    chain = prompt | llm | JsonOutputParser()
    
    try:
        triplets = chain.invoke({"text": latest_result[:2000]}) # Limit context for speed
        # Ensure it's a list
        if isinstance(triplets, dict):
            triplets = [triplets]
    except Exception as e:
        print(f"Extraction failed: {e}")
        triplets = []
        
    return {"graph_triplets": triplets}
