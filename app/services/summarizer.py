def summarize_text(text, mode="balanced"):
    # Placeholder (later replace with LLM)
    
    if mode == "quick":
        return text[:200]
    elif mode == "deep":
        return text[:500]
    
    return text[:300]