def classify_query(query):

    query = query.lower()

    troubleshooting_keywords = [
        "issue",
        "problem",
        "not working",
        "overheating",
        "battery",
        "error",
        "fix",
        "reset"
    ]

    comparison_keywords = [
        "compare",
        "difference",
        "vs",
        "better"
    ]

    if any(word in query for word in troubleshooting_keywords):
        return "troubleshooting"

    elif any(word in query for word in comparison_keywords):
        return "comparison"

    else:
        return "general"