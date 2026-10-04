from pydantic import BaseModel, Field
from typing import Optional, List

class TripIntent(BaseModel):
    destination: Optional[str] = Field(default=None, description="The intended destination.")
    duration: Optional[int] = Field(default=None, description="The intended duration in days.")
    origin: Optional[str] = Field(default=None, description="The starting location or origin.")
    budget: Optional[str] = Field(default=None, description="Budget preference (e.g., budget, moderate, luxury).")
    pace: Optional[str] = Field(default=None, description="Pace preference (e.g., relaxed, balanced, packed).")
    interests: List[str] = Field(default_factory=list, description="Specific interests (e.g., food, history, nature).")
    constraints: List[str] = Field(default_factory=list, description="Any hard constraints or requirements.")
    traveller_type: Optional[str] = Field(default=None, description="Type of traveller (e.g., solo, couple, family).")
    missing_information: List[str] = Field(default_factory=list, description="Crucial information that is missing and needed to plan the trip (e.g., destination, duration).")
