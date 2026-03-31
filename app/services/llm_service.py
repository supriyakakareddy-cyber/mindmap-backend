import os
import re
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def clean_output(output: str) -> str:
    output = re.sub(r"```json", "", output)
    output = re.sub(r"```", "", output)
    output = output.strip()

    match = re.search(r"\{.*\}", output, re.DOTALL)
    if match:
        return match.group(0)

    return output


def generate_mindmap_llm(text, mode="balanced"):

    prompt = f"""
    Convert the following content into a structured mind map.

    STRICT RULES:
    - Return ONLY valid JSON
    - No explanation
    - No markdown

    Format:
    {{
      "topic": "Main Topic",
      "children": [
        {{
          "title": "Subtopic",
          "children": []
        }}
      ]
    }}

    Content:
    {text}
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Return clean JSON only."},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=50  # 🔥 CRITICAL FIX (prevents hanging)
        )

        # 🔥 CHECK STATUS
        if response.status_code != 200:
            return json.dumps({
                "topic": "API Error",
                "children": [
                    {"title": f"Status: {response.status_code}"},
                    {"title": response.text[:100]}
                ]
            })

        data = response.json()

        if "error" in data:
            return json.dumps({
                "topic": "API Error",
                "children": [
                    {"title": data["error"].get("message", "Unknown error")}
                ]
            })

        choices = data.get("choices")
        if not choices:
            return json.dumps({
                "topic": "Error",
                "children": [
                    {"title": "No choices returned"},
                    {"title": str(data)}
                ]
            })

        raw_output = choices[0]["message"]["content"]

        cleaned = clean_output(raw_output)

        try:
            json.loads(cleaned)
            return cleaned
        except:
            return json.dumps({
                "topic": "Invalid JSON",
                "children": [
                    {"title": "Bad model output"},
                    {"title": cleaned[:100]}
                ]
            })

    except requests.exceptions.Timeout:
        return json.dumps({
            "topic": "Timeout Error",
            "children": [
                {"title": "LLM request took too long"}
            ]
        })

    except Exception as e:
        return json.dumps({
            "topic": "System Error",
            "children": [
                {"title": str(e)}
            ]
        })