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
        self.model_fast = os.environ.get("GEMINI_MODEL_FAST", "gemini-3.1-flash-lite")
        self.model_reasoning = os.environ.get("GEMINI_MODEL_REASONING", "gemini-3.1-flash-lite")

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[T],
        use_reasoning: bool = False,
        temperature: float = 0.2,
        retries: int = 3,
        timeout: float = 30.0,
        system_instruction: str = None
    ) -> T:
        """Generates structured output constrained to a Pydantic schema."""
        model = self.model_reasoning if use_reasoning else self.model_fast
        
        config_kwargs = {
            "response_mime_type": "application/json",
            "response_schema": schema,
            "temperature": temperature,
        }
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        config = types.GenerateContentConfig(**config_kwargs)

        try:
            from opentelemetry import trace
            from opentelemetry.trace import Status, StatusCode
            tracer = trace.get_tracer(__name__)
        except ImportError:
            tracer = None

        def create_span():
            if tracer:
                return tracer.start_as_current_span("gemini.generate_content")
            import contextlib
            return contextlib.nullcontext()

        with create_span() as span:
            if span and hasattr(span, 'set_attribute'):
                span.set_attribute("model", model)
                span.set_attribute("temperature", temperature)
                span.set_attribute("schema", schema.__name__)
                
            candidate_models = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-flash-lite-latest", model, "gemini-3.7-flash"]
            # Deduplicate preserving order
            seen_models = set()
            models_to_try = []
            for m in candidate_models:
                if m not in seen_models:
                    seen_models.add(m)
                    models_to_try.append(m)

            last_error = None
            for active_model in models_to_try:
                for attempt in range(retries):
                    try:
                        async with asyncio.timeout(timeout):
                            response = await self.client.aio.models.generate_content(
                                model=active_model,
                                contents=prompt,
                                config=config
                            )
                            if not response.text:
                                raise ValueError("Empty response text")
                            
                            if span and hasattr(span, 'set_attribute'):
                                if response.usage_metadata:
                                    span.set_attribute("usage.prompt_token_count", getattr(response.usage_metadata, 'prompt_token_count', 0))
                                    span.set_attribute("usage.candidates_token_count", getattr(response.usage_metadata, 'candidates_token_count', 0))
                                span.set_status(Status(StatusCode.OK))
                            
                            return schema.model_validate_json(response.text)
                    except asyncio.TimeoutError:
                        last_error = GeminiAPIError(f"Timeout on model {active_model}")
                        break
                    except Exception as e:
                        last_error = e
                        # If model is unavailable (503), not found (404), or quota exhausted (429), break immediately to try next model
                        err_str = str(e)
                        if any(k in err_str for k in ["429", "RESOURCE_EXHAUSTED", "Quota exceeded", "503", "404", "UNAVAILABLE", "NOT_FOUND"]):
                            break
                        await asyncio.sleep(1)

            if span and hasattr(span, 'set_status'):
                span.set_status(Status(StatusCode.ERROR, description=str(last_error)))
            raise GeminiAPIError(f"Gemini API Error: {str(last_error)}") from last_error

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
