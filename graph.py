from agents.planner import create_research_plan
from agents.researcher import conduct_research
from agents.analyst import analyze_research
from agents.report_generator import generate_research_outputs


def run_research_agent(topic, gemini_client):

    plan = create_research_plan(topic)

    research_data = conduct_research(topic)

    if not research_data:
        return {
            "plan": plan,
            "research": [],
            "analysis": {},
            "fact_check": "No research data available.",
            "report": "Unable to generate report."
        }

    analysis = analyze_research(research_data)

    fact_check = "Gemini API is unavailable."
    report = "Report generation is currently unavailable."

    try:
        outputs = generate_research_outputs(
            topic,
            research_data,
            gemini_client
        )

        fact_check = outputs["fact_check"]
        report = outputs["report"]

    except Exception as e:
        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            fact_check = "Gemini daily quota exceeded."
            report = "Please try again after the quota resets."

        elif "503" in error_message or "UNAVAILABLE" in error_message:
            fact_check = "Gemini server is temporarily busy."
            report = "Please try again later."

        else:
            fact_check = f"Fact checking unavailable: {error_message}"
            report = "Report generation failed."

    return {
        "plan": plan,
        "research": research_data,
        "analysis": analysis,
        "fact_check": fact_check,
        "report": report
    }