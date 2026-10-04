from pydantic import BaseModel
from typing import List

class FoodRecommendationResult(BaseModel):
    name: str
    cuisine: str
    price_category: str
    location: str
    opening_information: str
    confidence: float

class FoodList(BaseModel):
    recommendations: List[FoodRecommendationResult]
