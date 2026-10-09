try:
    from agents.common.tracing.decorators import trace_tool
except ImportError:
    def trace_tool(*args, **kwargs):
        return lambda f: f

from .common import ToolResult

@trace_tool()
async def search_transport(origin: str, destination: str, date: str) -> ToolResult:
    data = {"origin": origin, "destination": destination, "date": date, "options": ["Train", "Bus", "Flight"]}
    return ToolResult(success=True, data=data, source="mock_transport")
