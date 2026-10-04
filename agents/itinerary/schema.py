from pydantic import BaseModel, Field
from typing import List

class ItineraryItem(BaseModel):
    title: str = Field(description="Title of the activity")
    description: str = Field(description="Description of what to do")
    start_time: str = Field(description="Start time (e.g., 09:00)")
    end_time: str = Field(description="End time (e.g., 11:30)")
    location: str = Field(description="Geographic location or address")
    item_type: str = Field(description="e.g. Activity, Meal, Transit")

class TripDay(BaseModel):
    day_index: int = Field(description="Day number of the trip (1-indexed)")
    date: str = Field(description="Date of this itinerary day (YYYY-MM-DD)")
    theme_or_area: str = Field(description="General focus of this day")
    items: List[ItineraryItem] = Field(description="Chronological list of items")

class Itinerary(BaseModel):
    days: List[TripDay] = Field(description="List of all days in the itinerary")
