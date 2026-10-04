from pydantic import BaseModel, Field
from typing import Optional, List

class EffectiveTravellerPreferences(BaseModel):
    budget: Optional[str] = Field(default=None)
    pace: Optional[str] = Field(default=None)
    dietary_preferences: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    group_defaults: Optional[dict] = Field(default_factory=dict)
