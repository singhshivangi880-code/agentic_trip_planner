import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from agents.common.tracing.processor import RedactingSpanProcessor

def init_tracing(service_name="trip_planner_agents"):
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })
    
    provider = TracerProvider(resource=resource)
    
    otlp_endpoint = os.environ.get("OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    
    processor = BatchSpanProcessor(otlp_exporter)
    redacting_processor = RedactingSpanProcessor(processor)
    
    provider.add_span_processor(redacting_processor)
    trace.set_tracer_provider(provider)
