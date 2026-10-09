from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.trace import Span
import re

class RedactingSpanProcessor(SpanProcessor):
    def __init__(self, processor: SpanProcessor):
        self._processor = processor
        self.sensitive_patterns = [
            (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '[REDACTED_EMAIL]'),
            (re.compile(r'(?:\+)?\b[1-9]\d{4,14}\b'), '[REDACTED_PHONE]'),
            (re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})\b'), '[REDACTED_PAYMENT]'),
            (re.compile(r'(?i)\b(?:Bearer\s+|api_key=)[a-zA-Z0-9_\-.]+\b'), '[REDACTED_AUTH]'),
            (re.compile(r'\b[A-Z0-9]{6,8}\b'), '[REDACTED_BOOKING]'),
        ]

    def _redact(self, value: str) -> str:
        if not isinstance(value, str):
            return value
        for pattern, replacement in self.sensitive_patterns:
            value = pattern.sub(replacement, value)
        return value

    def on_start(self, span: Span, parent_context=None):
        self._processor.on_start(span, parent_context)

    def on_end(self, span):
        if hasattr(span, '_attributes') and span._attributes:
            from opentelemetry.attributes import BoundedAttributes
            new_attrs = {}
            for k, v in span._attributes.items():
                if isinstance(v, str):
                    new_attrs[k] = self._redact(v)
                else:
                    new_attrs[k] = v
            # Create a new BoundedAttributes to replace the immutable one
            span._attributes = BoundedAttributes(
                maxlen=span._attributes.maxlen,
                attributes=new_attrs,
                immutable=True,
                max_value_len=span._attributes.max_value_len
            )
        self._processor.on_end(span)

    def shutdown(self):
        self._processor.shutdown()

    def force_flush(self, timeout_millis=30000):
        self._processor.force_flush(timeout_millis)
