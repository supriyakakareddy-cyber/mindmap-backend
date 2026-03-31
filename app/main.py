from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.schemas import MindMapRequest
from app.services.processor import process_input
from app.services.llm_service import generate_mindmap_llm
import json
import os
import uuid

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CREATE FOLDER FOR FILES
os.makedirs("mindmaps", exist_ok=True)

# ✅ SERVE FILES AS URL
app.mount("/mindmaps", StaticFiles(directory="mindmaps"), name="mindmaps")


@app.get("/")
def home():
    return {"message": "Mind Map Agent is running 🚀"}


@app.post("/generate-mindmap")
def generate_mindmap(request: MindMapRequest):

    print("🔥 REQUEST RECEIVED")

    try:
        processed = process_input(request)

        if processed["status"] == "need_user_input":
            return processed

        text = processed["clean_text"]

        print("📄 Processing text...")

        # 🔥 CALL LLM
        llm_output = generate_mindmap_llm(text, request.mode)

        print("🤖 LLM OUTPUT RECEIVED")

        try:
            mindmap = json.loads(llm_output)
        except Exception:
            return {
                "status": "error",
                "message": "Invalid JSON from LLM",
                "raw_output": llm_output
            }

        # ✅ SAVE FILE (NEW PART)
        file_id = str(uuid.uuid4())
        file_path = f"mindmaps/{file_id}.json"

        with open(file_path, "w") as f:
            json.dump(mindmap, f)

        # ✅ RETURN URL + DATA
        return {
            "status": "success",
            "summary": "Generated using AI",
            "mindmap": mindmap,
            "url": f"http://localhost:8000/mindmaps/{file_id}.json"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }