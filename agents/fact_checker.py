from utils.helpers import generate_with_retry


def check_facts(research_data, gemini_client):

    if not research_data:
        return "No research data available."

    if not gemini_client:
        return "Gemini client is not connected."

    research_text = ""

    for item in research_data:
        research_text += (
            f"\nTitle: {item.get('title', '')}\n"
            f"Content: {item.get('content', '')}\n"
            f"URL: {item.get('url', '')}\n"
        )

    prompt = f"""
    You are an expert research fact-checking assistant.

    Review the following research information:

    {research_text}

    Check:
    1. Accuracy and consistency
    2. Unsupported claims
    3. Contradictory information
    4. Missing evidence

    Do not invent facts.
    Mention when information cannot be verified.
    """

    response = generate_with_retry(gemini_client, prompt)

    return response or "Fact-checking response is empty."