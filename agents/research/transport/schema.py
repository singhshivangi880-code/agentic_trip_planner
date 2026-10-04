from pydantic import BaseModel
from typing import List

class TransportOption(BaseModel):
    mode: str
    departure: str
    arrival: str
    duration_hours: float
    booking_information: str
    is_stale_data: bool
    confidence: float

class TransportList(BaseModel):
    options: List[TransportOption]
