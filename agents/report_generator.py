from utils.helpers import generate_with_retry


def generate_research_outputs(topic, research_data, gemini_client):

    # Check research topic
    if not topic or not topic.strip():
        return {
            "fact_check": "Research topic is missing.",
            "report": "Unable to generate report without a topic."
        }

    # Check research data
    if not research_data:
        return {
            "fact_check": "No research data available.",
            "report": "No research data available."
        }

    # Check Gemini connection
    if not gemini_client:
        return {
            "fact_check": "Gemini client is not connected.",
            "report": "Gemini client is not connected."
        }

    # Prepare research information
    research_sections = []

    for index, item in enumerate(research_data, 1):

        if not isinstance(item, dict):
            continue

        title = item.get("title", "Untitled Source")
        content = item.get("content", "")
        url = item.get("url", "")

        research_sections.append(
            f"""
            Source {index}
            Title: {title}
            Content: {content}
            URL: {url}
            """
        )

    if not research_sections:
        return {
            "fact_check": "No valid research sources found.",
            "report": "Unable to generate report."
        }

    research_text = "\n\n".join(research_sections)

    # Prepare Gemini prompt
    prompt = f"""
    You are an expert research assistant.

    Research Topic: {topic.strip()}

    Research Information:
    {research_text}

    Complete BOTH tasks in one response.

    TASK 1: FACT CHECKING

    Write:

    FACT_CHECK:

    - Check the accuracy of important claims.
    - Identify unsupported statements.
    - Identify contradictions between sources.
    - Mention missing evidence.
    - Do not invent facts.

    TASK 2: RESEARCH REPORT

    Write:

    RESEARCH_REPORT:

    1. Introduction
    2. Key Findings
    3. Current Trends
    4. Applications
    5. Advantages
    6. Challenges
    7. Future Scope
    8. Conclusion
    9. References

    Instructions:
    - Use simple professional language.
    - Include relevant source URLs.
    - Use the provided research information.
    - Do not invent facts or references.
    - Clearly distinguish verified information
      from uncertain claims.
    """

    # Generate response using Gemini
    response = generate_with_retry(
        gemini_client,
        prompt
    )

    if not response or not response.strip():
        return {
            "fact_check": "Gemini returned an empty response.",
            "report": "Report generation failed."
        }

    # Separate fact-check and report
    parts = response.split("RESEARCH_REPORT:", 1)

    fact_check = (
        parts[0].replace("FACT_CHECK:", "").strip()
    )

    report = (
        parts[1].strip()
        if len(parts) > 1
        else response.strip()
    )

    return {
        "fact_check": fact_check,
        "report": report
    }