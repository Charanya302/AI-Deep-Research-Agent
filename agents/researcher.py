from tools.web_search import search_web


def conduct_research(topic):

    print("Research started...")

    results = search_web(topic, max_results=5)

    if not results:
        return []

    research_data = []

    for result in results:

        research_data.append({
            "title": result.get("title", ""),
            "content": result.get("content", ""),
            "url": result.get("url", "")
        })

    print(f"Research completed! {len(research_data)} sources found.")

    return research_data