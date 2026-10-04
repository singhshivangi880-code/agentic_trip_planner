import pytest
from tools.search import search, fetch
from tools.places import get_place, get_opening_hours
from tools.maps import get_route, get_distance_matrix
from tools.weather import get_weather, get_forecast
from tools.transport import search_transport

@pytest.mark.asyncio
async def test_search():
    res = await search("hotels in Tokyo")
    assert res.success is True
    assert res.source == "mock_search"
    assert "Tokyo" in res.data["query"]

@pytest.mark.asyncio
async def test_fetch():
    res = await fetch("http://example.com")
    assert res.success is True
    assert res.source == "mock_fetch"

@pytest.mark.asyncio
async def test_places():
    res = await get_place("place123")
    assert res.success is True
    assert res.data["place_id"] == "place123"
    
    res2 = await get_opening_hours("place123")
    assert res2.success is True

@pytest.mark.asyncio
async def test_maps():
    res = await get_route("A", "B")
    assert res.success is True
    
    res2 = await get_distance_matrix(["A", "B"])
    assert res2.success is True

@pytest.mark.asyncio
async def test_weather():
    res = await get_weather("Tokyo", "2026-10-10")
    assert res.success is True
    
    res2 = await get_forecast("Tokyo")
    assert res2.success is True

@pytest.mark.asyncio
async def test_transport():
    res = await search_transport("Tokyo", "Kyoto", "2026-10-10")
    assert res.success is True
    assert "Train" in res.data["options"]
