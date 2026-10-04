from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationItem(BaseModel):
    name: str = Field(description="Name of the activity, restaurant, or place")
    category: str = Field(description="Type of recommendation (e.g. food, experience, attraction)")
    reason: str = Field(description="Why this is recommended for this specific user")
    score: int = Field(description="Overall recommendation score from 1-100")
    time_of_day_suitability: List[str] = Field(description="e.g. morning, afternoon, evening")
    tourist_or_offbeat: str = Field(description="Is this a typical tourist trap or an offbeat location?")
    source_reference: Optional[str] = Field(default=None, description="Original source name if available")

class RecommendationList(BaseModel):
    recommendations: List[RecommendationItem]
