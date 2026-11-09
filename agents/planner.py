def create_research_plan(topic):
    
    if not topic.strip():
        return []

    plan = [
        {
            "step": 1,
            "task": f"Understand the research topic: {topic}"
        },
        {
            "step": 2,
            "task": "Identify important concepts and keywords"
        },
        {
            "step": 3,
            "task": "Search for reliable information"
        },
        {
            "step": 4,
            "task": "Collect relevant facts and findings"
        },
        {
            "step": 5,
            "task": "Analyze the collected information"
        },
        {
            "step": 6,
            "task": "Prepare a detailed research report"
        }
    ]

    return plan