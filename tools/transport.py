from .common import ToolResult

async def search_transport(origin: str, destination: str, date: str) -> ToolResult:
    data = {"origin": origin, "destination": destination, "date": date, "options": ["Train", "Bus", "Flight"]}
    return ToolResult(success=True, data=data, source="mock_transport")
