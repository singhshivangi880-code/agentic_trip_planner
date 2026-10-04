from .common import ToolResult

async def get_route(origin: str, destination: str) -> ToolResult:
    data = {"origin": origin, "destination": destination, "distance_km": 15, "duration_mins": 30}
    return ToolResult(success=True, data=data, source="mock_maps")

async def get_distance_matrix(locations: list[str]) -> ToolResult:
    data = {"locations": locations, "matrix": [[0, 10], [10, 0]]}
    return ToolResult(success=True, data=data, source="mock_maps")
