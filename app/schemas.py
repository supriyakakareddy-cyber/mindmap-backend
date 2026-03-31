from pydantic import BaseModel
from typing import List, Optional

class MindMapRequest(BaseModel):
    input_type: str  # "text" or "file"
    content: str
    pages: Optional[List[int]] = None
    mode: Optional[str] = "balanced"

class MindMapResponse(BaseModel):
    status: str
    summary: Optional[str] = None
    mindmap: Optional[dict] = None
    pages_preview: Optional[List[str]] = None