def analyze_research(research_data):
    
    # Check whether research data is available
    if not research_data:
        return {
            "total_sources": 0,
            "main_topics": [],
            "source_urls": [],
            "summary": "No research data available."
        }

    main_topics = []
    source_urls = []
    summaries = []

    # Process each research source
    for item in research_data:

        if not isinstance(item, dict):
            continue

        title = item.get("title", "").strip()
        url = item.get("url", "").strip()
        content = item.get("content", "").strip()

        # Collect source titles without duplicates
        if title and title not in main_topics:
            main_topics.append(title)

        # Collect unique source URLs
        if url and url not in source_urls:
            source_urls.append(url)

        # Collect research content
        if content:
            summaries.append(content)

    # Combine collected information
    summary = "\n\n".join(summaries)

    # Return structured analysis
    analysis = {
        "total_sources": len(research_data),
        "main_topics": main_topics,
        "source_urls": source_urls,
        "summary": summary
    }

    return analysis