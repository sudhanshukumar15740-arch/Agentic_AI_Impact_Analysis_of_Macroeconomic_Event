import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_news(query: str) -> str:
    """Search the web for recent news and information about a topic."""
    res = client.search(query=query, max_results=5, topic="news")
    return "\n\n".join(
        f"- {r['title']}: {r['content']} (source: {r['url']})"
        for r in res["results"]
    )