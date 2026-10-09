import re
from typing import Any, Dict

def sanitize_input(text: str) -> str:
    """Sanitize external content to prevent prompt injection."""
    if not text:
        return text
        
    injection_patterns = [
        r"(?i)ignore\s+(all\s+)?previous\s+instructions",
        r"(?i)system\s+prompt",
        r"(?i)you\s+are\s+now",
        r"(?i)forget\s+(everything|all)",
        r"(?i)bypass\s+filters",
        r"(?i)disregard"
    ]
    
    sanitized = text
    for pattern in injection_patterns:
        sanitized = re.sub(pattern, "[FILTERED]", sanitized)
        
    return sanitized

def validate_structured_output(schema, data: dict):
    """Validate data against a Pydantic schema."""
    return schema.model_validate(data)
