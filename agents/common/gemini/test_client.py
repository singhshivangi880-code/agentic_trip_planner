import pytest
import asyncio
from pydantic import BaseModel
from agents.common.gemini.client import GeminiClient, MockGeminiClient, GeminiAPIError

class DummySchema(BaseModel):
    response: str
    confidence: float

@pytest.mark.asyncio
async def test_mock_gemini_client():
    mock_client = MockGeminiClient()
    
    # Set up mock response
    expected = DummySchema(response="test", confidence=0.99)
    mock_client.set_mock_response(DummySchema, expected)
    
    result = await mock_client.generate_structured("prompt", DummySchema)
    assert result.response == "test"
    assert result.confidence == 0.99
    
    # Test fallback
    class UnmockedSchema(BaseModel):
        field: str = "default"
        
    fallback_result = await mock_client.generate_structured("prompt", UnmockedSchema)
    assert fallback_result.field == "default"
