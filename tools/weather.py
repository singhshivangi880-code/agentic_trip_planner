try:
    from agents.common.tracing.decorators import trace_tool
except ImportError:
    def trace_tool(*args, **kwargs):
        return lambda f: f

from .common import ToolResult

@trace_tool()
async def get_weather(location: str, date: str) -> ToolResult:
    data = {"location": location, "date": date, "temp_c": 22, "condition": "Sunny"}
    return ToolResult(success=True, data=data, source="mock_weather")

@trace_tool()
async def get_forecast(location: str) -> ToolResult:
    data = {"location": location, "forecast": ["Sunny", "Rainy", "Cloudy"]}
    return ToolResult(success=True, data=data, source="mock_weather")
