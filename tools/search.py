from .common import ToolResult

async def search(query: str, location: str = None) -> ToolResult:
    # ponytail: minimal deterministic mock
    data = {"query": query, "location": location, "results": [f"Mock search result for {query}"]}
    return ToolResult(success=True, data=data, source="mock_search")

async def fetch(url: str) -> ToolResult:
    data = {"url": url, "content": "Mock page content."}
    return ToolResult(success=True, data=data, source="mock_fetch")
