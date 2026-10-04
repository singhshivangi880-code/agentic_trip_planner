from pydantic import BaseModel, Field
from typing import List, Optional

class AttractionCategory(BaseModel):
    primary: str
    tags: List[str]

class LocationInfo(BaseModel):
    name: str
    address: str
    coordinates: Optional[str] = None

class AttractionResult(BaseModel):
    name: str
    category: AttractionCategory
    estimated_duration_hours: float
    location: LocationInfo
    opening_hours: List[str]
    confidence: float

class AttractionList(BaseModel):
    attractions: List[AttractionResult]
