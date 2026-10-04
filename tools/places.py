from .common import ToolResult

async def get_place(place_id: str) -> ToolResult:
    data = {"place_id": place_id, "name": "Mock Place", "rating": 4.5}
    return ToolResult(success=True, data=data, source="mock_places")

async def get_opening_hours(place_id: str) -> ToolResult:
    data = {"place_id": place_id, "hours": ["Monday: 9AM-5PM", "Tuesday: 9AM-5PM"]}
    return ToolResult(success=True, data=data, source="mock_places")
