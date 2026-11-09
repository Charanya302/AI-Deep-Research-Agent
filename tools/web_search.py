import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Get Tavily API key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_web(query, max_results=5):

    if not TAVILY_API_KEY:
        raise ValueError("Tavily API key is missing!")

    # Initialize Tavily client
    tavily_client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    # Search the web
    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    # Extract results
    results = response.get("results", [])

    return results


def format_search_results(results):

    research_data = ""

    for i, result in enumerate(results, start=1):

        research_data += (
            f"\nSource {i}\n"
            f"Title: {result.get('title', '')}\n"
            f"Content: {result.get('content', '')}\n"
            f"URL: {result.get('url', '')}\n"
        )

    return research_data