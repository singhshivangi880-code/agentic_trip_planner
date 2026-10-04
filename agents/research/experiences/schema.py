from pydantic import BaseModel
from typing import List

class ExperienceResult(BaseModel):
    name: str
    category: str
    description: str
    tourist_or_offbeat: str
    confidence: float

class ExperienceList(BaseModel):
    experiences: List[ExperienceResult]
