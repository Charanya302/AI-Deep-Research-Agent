def analyze_research(research_data):
    
    if not research_data:
        return {
            "total_sources": 0,
            "main_topics": [],
            "source_urls": [],
            "summary": "No research data available."
        }

    analysis = {
        "total_sources": len(research_data),
        "main_topics": [],
        "source_urls": [],
        "summary": ""
    }

    for item in research_data:

        title = item.get("title", "")
        url = item.get("url", "")
        content = item.get("content", "")

        if title:
            analysis["main_topics"].append(title)

        if url:
            analysis["source_urls"].append(url)

        if content:
            analysis["summary"] += content + "\n"

    return analysis