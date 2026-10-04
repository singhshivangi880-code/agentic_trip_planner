import os
import asyncio
from typing import Type, Optional, TypeVar
from pydantic import BaseModel
from google import genai
from google.genai import types

T = TypeVar('T', bound=BaseModel)

class GeminiAPIError(Exception):
    """Mapped application error for Gemini provider issues."""
    pass

class GeminiClient:
    """Wrapper for the Gemini SDK handling structured output, retries, and timeouts."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_fast = os.environ.get("GEMINI_MODEL_FAST", "gemini-2.5-flash")
        self.model_reasoning = os.environ.get("GEMINI_MODEL_REASONING", "gemini-2.5-pro")

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        use_reasoning: bool = False,
        temperature: float = 0.2,
        retries: int = 3,
        timeout: float = 30.0
    ) -> T:
        """Generates structured output constrained to a Pydantic schema."""
        model = self.model_reasoning if use_reasoning else self.model_fast
        
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=temperature,
        )

        for attempt in range(retries):
            try:
                # ponytail: built-in asyncio.timeout is simpler than tenacity for 3 lines of retry logic
                async with asyncio.timeout(timeout):
                    response = await self.client.aio.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config
                    )
                    if not response.text:
                        raise ValueError("Empty response text")
                    return schema.model_validate_json(response.text)
            except asyncio.TimeoutError:
                if attempt == retries - 1:
                    raise GeminiAPIError(f"Timeout after {retries} attempts")
            except Exception as e:
                # Map provider errors to our domain exception
                if attempt == retries - 1:
                    raise GeminiAPIError(f"Gemini API Error: {str(e)}") from e
                
            await asyncio.sleep(2 ** attempt)

class MockGeminiClient:
    """Test double for GeminiClient."""
    def __init__(self, *args, **kwargs):
        self.responses = {}

    def set_mock_response(self, schema_cls: Type[BaseModel], response: BaseModel):
        self.responses[schema_cls] = response

    async def generate_structured(self, prompt: str, schema: Type[T], **kwargs) -> T:
        if schema in self.responses:
            return self.responses[schema]
        # ponytail: fallback empty model construction for mocks without strict typing checks
        return schema.model_construct()
