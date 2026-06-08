from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import AgentState



REPORTER_PROMPT = """
You are a Senior Research Analyst.
Write a comprehensive, professional report on: {task}

Sources:
{research_results}

Knowledge Graph Facts:
{graph_triplets}

Guidelines:
1. ZERO HALLUCINATION POLICY: You may ONLY write about facts present in the Sources or Knowledge Graph.
2. If information is missing for a section, write "Data not available in search results." DO NOT invent it.
3. Citations: Every single claim must have a [Source-ID] or mention the source name.
4. Tone: Technical, precise, and dry. Avoid "fluff" or "filler" content.
5. Structure:
   - **Executive Summary**
   - **Key Findings** (Bullet points with data)
   - **Detailed Analysis** (Structured sections)
   - **References** (List of Links/Sources used)
6. FORMAT: Return the report in clean Markdown. Use hyperlinks [Title](URL) if URLs are available in the logs.

Write the full report now.
"""

def reporter_node(state: AgentState):

    prompt = ChatPromptTemplate.from_template(REPORTER_PROMPT)
    model_name = state.get("model_name", "gemini-3-flash-preview")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
    chain = prompt | llm | StrOutputParser()
    
    report = chain.invoke({
        "task": state["task"],
        "research_results": "\n\n".join(state.get("research_results", [])),
        "graph_triplets": str(state.get("graph_triplets", [])),
    })
    
    return {"final_report": report}
