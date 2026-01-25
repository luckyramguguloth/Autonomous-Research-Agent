from typing import List, Dict, Optional
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

@tool
def web_search(query: str, max_results: int = 3) -> str:
    """
    Performs a web search using DuckDuckGo and returns the results.
    Useful for finding current information, news, or general knowledge.
    
    Args:
        query: The search query string.
        max_results: The maximum number of results to return.
    """
    search = DuckDuckGoSearchResults(backend="text", max_results=max_results)
    try:
        results = search.run(query)
        return results
    except Exception as e:
        return f"Error executing search: {str(e)}"
