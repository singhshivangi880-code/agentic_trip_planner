from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

class ToolResult(BaseModel):
    success: bool
    data: Any = None
    source: str
    retrieved_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence: float = 1.0
    error: Optional[str] = None
