try:
    from agents.common.tracing.decorators import trace_tool
except ImportError:
    def trace_tool(*args, **kwargs):
        return lambda f: f

from .common import ToolResult

@trace_tool()
async def get_place(place_id: str) -> ToolResult:
    data = {"place_id": place_id, "name": "Mock Place", "rating": 4.5}
    return ToolResult(success=True, data=data, source="mock_places")

@trace_tool()
async def get_opening_hours(place_id: str) -> ToolResult:
    data = {"place_id": place_id, "hours": ["Monday: 9AM-5PM", "Tuesday: 9AM-5PM"]}
    return ToolResult(success=True, data=data, source="mock_places")
