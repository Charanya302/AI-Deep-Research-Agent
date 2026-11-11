def create_research_plan(topic):
    
    # Check whether the topic is empty
    if not topic or not topic.strip():
        return []

    # Create a structured research plan
    plan = [
        {
            "step": 1,
            "task": f"Understand the research topic: {topic.strip()}"
        },
        {
            "step": 2,
            "task": "Identify key concepts, keywords and research questions"
        },
        {
            "step": 3,
            "task": "Search the web for reliable and relevant information"
        },
        {
            "step": 4,
            "task": "Collect important facts, evidence and source references"
        },
        {
            "step": 5,
            "task": "Analyze the collected information and identify key findings"
        },
        {
            "step": 6,
            "task": "Verify important facts and check information reliability"
        },
        {
            "step": 7,
            "task": "Prepare a structured and detailed research report"
        }
    ]

    return plan