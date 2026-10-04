from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta

def default_expiry():
    return datetime.now(timezone.utc) + timedelta(hours=24)

class DecisionCheckpoint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str = Field(description="Question to present to the user")
    context: dict = Field(default_factory=dict, description="Contextual data for the decision")
    options: List[str] = Field(description="List of allowed responses")
    default_option: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=default_expiry)
