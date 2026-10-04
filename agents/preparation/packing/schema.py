from pydantic import BaseModel, Field

class PackingItem(BaseModel):
    name: str = Field(description="Name of the item")
    reason: str = Field(description="Why this item is needed based on weather or activities")
    is_essential: bool = Field(description="Is this absolutely required?")

class PackingCategory(BaseModel):
    category_name: str = Field(description="E.g., Clothing, Electronics, Documents, Activity-specific")
    items: list[PackingItem]

class PackingList(BaseModel):
    categories: list[PackingCategory]
    assumptions_made: list[str] = Field(description="Any assumptions made about the user's base items")
