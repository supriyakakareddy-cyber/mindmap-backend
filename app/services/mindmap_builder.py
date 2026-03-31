def build_mindmap(summary):
    # Simple structured output (LLM later)

    return {
        "topic": "Main Topic",
        "children": [
            {
                "title": "Key Idea 1",
                "children": [
                    {"title": "Detail A"},
                    {"title": "Detail B"}
                ]
            },
            {
                "title": "Key Idea 2",
                "children": [
                    {"title": "Detail C"},
                    {"title": "Detail D"}
                ]
            }
        ]
    }