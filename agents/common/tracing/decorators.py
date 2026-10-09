import functools
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import inspect

tracer = trace.get_tracer(__name__)

def trace_agent(name=None):
    def decorator(func):
        span_name = name or func.__name__
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(self, state, *args, **kwargs):
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("agent.name", span_name)
                    # Trace context propagation
                    if hasattr(state, 'get'):
                        span.set_attribute("workflow.status", str(state.get("workflow_status", "")))
                        span.set_attribute("workflow.trip_id", str(state.get("trip", {}).get("id", "")))
                    try:
                        result = await func(self, state, *args, **kwargs)
                        if hasattr(result, 'status'):
                            if result.status == "failed":
                                span.set_status(Status(StatusCode.ERROR, description=str(getattr(result, 'metadata', {}).get("error", ""))))
                            else:
                                span.set_status(Status(StatusCode.OK))
                        return result
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.record_exception(e)
                        raise
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(self, state, *args, **kwargs):
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute("agent.name", span_name)
                    if hasattr(state, 'get'):
                        span.set_attribute("workflow.status", str(state.get("workflow_status", "")))
                        span.set_attribute("workflow.trip_id", str(state.get("trip", {}).get("id", "")))
                    try:
                        result = func(self, state, *args, **kwargs)
                        if hasattr(result, 'status'):
                            if result.status == "failed":
                                span.set_status(Status(StatusCode.ERROR, description=str(getattr(result, 'metadata', {}).get("error", ""))))
                            else:
                                span.set_status(Status(StatusCode.OK))
                        return result
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.record_exception(e)
                        raise
            return sync_wrapper
    return decorator

def trace_tool(name=None):
    def decorator(func):
        span_name = name or func.__name__
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                with tracer.start_as_current_span(f"tool.{span_name}") as span:
                    span.set_attribute("tool.name", span_name)
                    try:
                        result = await func(*args, **kwargs)
                        return result
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.record_exception(e)
                        raise
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with tracer.start_as_current_span(f"tool.{span_name}") as span:
                    span.set_attribute("tool.name", span_name)
                    try:
                        result = func(*args, **kwargs)
                        return result
                    except Exception as e:
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.record_exception(e)
                        raise
            return sync_wrapper
    return decorator
