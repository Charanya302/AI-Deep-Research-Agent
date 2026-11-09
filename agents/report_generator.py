from utils.helpers import generate_with_retry


def generate_research_outputs(topic, research_data, gemini_client):

    if not research_data:
        return {
            "fact_check": "No research data available.",
            "report": "No research data available."
        }

    if not gemini_client:
        return {
            "fact_check": "Gemini client is not connected.",
            "report": "Gemini client is not connected."
        }

    research_text = ""

    for item in research_data:
        research_text += (
            f"\nTitle: {item.get('title', '')}\n"
            f"Content: {item.get('content', '')}\n"
            f"URL: {item.get('url', '')}\n"
        )

    prompt = f"""
    You are an expert research assistant.

    Research Topic: {topic}

    Research Information:
    {research_text}

    Complete BOTH tasks in one response.

    First, write:

    FACT_CHECK:
    Check accuracy, unsupported claims, contradictions,
    and missing evidence. Do not invent facts.

    Second, write:

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

    Use simple professional language.
    Include source URLs.
    Do not invent facts.
    """

    response = generate_with_retry(gemini_client, prompt)

    if not response:
        response = "Gemini returned an empty response."

    parts = response.split("RESEARCH_REPORT:", 1)

    fact_check = parts[0].replace("FACT_CHECK:", "").strip()

    report = parts[1].strip() if len(parts) > 1 else response

    return {
        "fact_check": fact_check,
        "report": report
    }