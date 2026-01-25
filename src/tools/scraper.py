import trafilatura
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def scrape_content(url: str) -> str:
    """
    Extracts the main text content from a given URL.
    Useful for reading article content, blog posts, or documentation.
    
    Args:
        url: The URL to scrape.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text:
                return text
        
        # Fallback to simple BS4 if trafilatura fails or returns None
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:5000] # Limit content length for speed
        
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
