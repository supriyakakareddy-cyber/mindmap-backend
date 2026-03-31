def process_input(request):
    content = request.content
    
    # Define a safe limit based on OpenRouter/GPT-4o-mini capabilities
  
    MAX_CHARS = 50000 

    if len(content) > MAX_CHARS:
        return {
            "status": "error",
            "message": "Too long text request denied! Please reduce the input size."
        }

    # If within limits, bypass the "Multiple Topics" selection and go straight to mapping
    return {
        "status": "ok",
        "clean_text": content
    }