from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from agents.planner import create_research_plan
from agents.researcher import conduct_research
from agents.analyst import analyze_research
from agents.report_generator import generate_research_outputs

from rag.retriever import retrieve_documents


# ==========================================
# 1. RESEARCH STATE
# ==========================================

class ResearchState(TypedDict, total=False):

    topic: str
    gemini_client: Any
    plan: list
    research: list
    analysis: dict
    rag_context: str
    fact_check: str
    report: str


# ==========================================
# 2. PLANNER AGENT
# ==========================================

def planner_node(state: ResearchState):

    topic = state["topic"]

    plan = create_research_plan(topic)

    print("\nResearch plan created successfully!")

    return {"plan": plan}


# ==========================================
# 3. RESEARCHER AGENT
# ==========================================

def researcher_node(state: ResearchState):

    topic = state["topic"]

    research_data = conduct_research(topic)

    return {"research": research_data}


# ==========================================
# 4. ANALYST AGENT
# ==========================================

def analyst_node(state: ResearchState):

    research_data = state.get("research", [])

    analysis = analyze_research(research_data)

    print("\nResearch analysis completed!")

    return {"analysis": analysis}


# ==========================================
# 5. RAG RETRIEVER NODE
# ==========================================

def rag_retriever_node(state: ResearchState):

    topic = state["topic"]

    try:

        documents = retrieve_documents(topic, k=3)

        rag_context = "\n\n".join(
            doc.page_content for doc in documents
        )

        print("\nRAG document retrieval completed!")

        return {"rag_context": rag_context}

    except Exception as e:

        print("RAG retrieval error:", str(e))

        return {"rag_context": ""}


# ==========================================
# 6. REPORT GENERATOR AGENT
# ==========================================

def report_node(state: ResearchState):

    try:

        outputs = generate_research_outputs(
            state["topic"],
            state.get("research", []),
            state.get("gemini_client"),
            state.get("rag_context", "")
        )

        return {
            "fact_check": outputs["fact_check"],
            "report": outputs["report"]
        }

    except Exception as e:

        print("Report generation error:", str(e))

        return {
            "fact_check": f"Fact checking unavailable: {str(e)}",
            "report": "Report generation failed."
        }


# ==========================================
# 7. CONDITIONAL ROUTING
# ==========================================

def route_after_research(state: ResearchState):
    
    research_data = state.get("research", [])

    if research_data:
        print("\nResearch sources found. Continuing workflow.")
        return "continue"

    print("\nNo web research sources found. Continuing to RAG.")

    return "continue"


# ==========================================
# 8. CREATE LANGGRAPH WORKFLOW
# ==========================================

workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner_node)

workflow.add_node("researcher", researcher_node)

workflow.add_node("analyst", analyst_node)

workflow.add_node("rag_retriever", rag_retriever_node)

workflow.add_node("report_generator", report_node)


# Connect nodes

workflow.add_edge(START, "planner")

workflow.add_edge("planner", "researcher")


workflow.add_conditional_edges(
    "researcher",
    route_after_research,
    {
        "continue": "analyst",
        "stop": END
    }
)

workflow.add_edge("analyst", "rag_retriever")

workflow.add_edge("rag_retriever", "report_generator")

workflow.add_edge("report_generator", END)


# ==========================================
# 9. COMPILE WORKFLOW
# ==========================================

research_graph = workflow.compile()


# ==========================================
# 10. MAIN RESEARCH FUNCTION
# ==========================================

def run_research_agent(topic, gemini_client):

    if not topic or not topic.strip():

        raise ValueError("Research topic cannot be empty.")

    initial_state = {

        "topic": topic.strip(),

        "gemini_client": gemini_client

    }

    result = research_graph.invoke(initial_state)

    if not result.get("research"):

        result["analysis"] = {}

        result["fact_check"] = "No research data available."

        result["report"] = "Unable to generate report."

    return result