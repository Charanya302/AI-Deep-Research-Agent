import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Get Tavily API key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_web(query, max_results=5):

    # Validate API key
    if not TAVILY_API_KEY:
        raise ValueError("Tavily API key is missing!")

    # Validate search query
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    # Validate maximum results
    if not isinstance(max_results, int) or max_results < 1:
        raise ValueError("max_results must be a positive integer.")

    # Initialize Tavily client
    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    # Search the web
    response = tavily_client.search(
        query=query.strip(),
        search_depth="basic",
        max_results=max_results
    )

    # Extract search results
    results = response.get("results", [])

    if not isinstance(results, list):
        return []

    return results


def format_search_results(results):

    if not results:
        return "No search results available."

    research_data = []

    for i, result in enumerate(results, start=1):

        if not isinstance(result, dict):
            continue

        research_data.append(
            f"""
Source {i}
Title: {result.get('title', 'Untitled Source')}
Content: {result.get('content', '')}
URL: {result.get('url', '')}
"""
        )

    return "\n".join(research_data)