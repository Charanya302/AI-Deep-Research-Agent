from tools.web_search import search_web


def conduct_research(topic):

    # Check empty research topic
    if not topic or not topic.strip():
        print("Research topic is empty.")
        return []

    print(f"Research started for: {topic}")

    try:
        # Search the web using Tavily
        results = search_web(topic.strip(), max_results=5)

        if not results:
            print("No research sources found.")
            return []

        research_data = []

        # Process search results
        for result in results:

            if not isinstance(result, dict):
                continue

            research_data.append({
                "title": result.get("title", "Untitled Source"),
                "content": result.get("content", ""),
                "url": result.get("url", "")
            })

        print(
            f"Research completed! "
            f"{len(research_data)} sources found."
        )

        return research_data

    except Exception as e:

        print(f"Research error: {e}")
        raise