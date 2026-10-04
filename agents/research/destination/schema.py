from pydantic import BaseModel, Field
from typing import List, Optional

class CityCandidate(BaseModel):
    name: str
    description: str
    pros: List[str]
    cons: List[str]

class Seasonality(BaseModel):
    best_time_to_visit: str
    weather_expected: str

class TravelConsideration(BaseModel):
    category: str  # e.g., Safety, Health, Visas, Logistics
    details: str

class DestinationOverview(BaseModel):
    destination: str
    overview: str
    cities: List[CityCandidate]
    seasonality: Seasonality
    considerations: List[TravelConsideration]
