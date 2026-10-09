from fastapi import APIRouter, HTTPException, Depends
import httpx
from pydantic import BaseModel
from typing import Any
from app.core.security import require_dev, rate_limit

router = APIRouter(prefix="/dev", tags=["dev"])

JAEGER_API_URL = "http://localhost:16686/api"

@router.get("/traces/{trace_id}", dependencies=[Depends(require_dev), rate_limit(times=100, seconds=60)])
async def get_trace(trace_id: str) -> Any:
    """
    Fetch a trace from local Jaeger, formatting it into a simplified timeline view
    for the developer trace viewer.
    """
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{JAEGER_API_URL}/traces/{trace_id}")
            if resp.status_code == 404:
                raise HTTPException(status_code=404, detail="Trace not found in Jaeger")
            resp.raise_for_status()
            
            data = resp.json()
            if not data.get("data"):
                raise HTTPException(status_code=404, detail="Trace not found")
                
            trace_data = data["data"][0]
            
            # Format the raw Jaeger trace into a timeline
            spans = trace_data.get("spans", [])
            processes = trace_data.get("processes", {})
            
            # Create a span dictionary for parent lookup
            span_dict = {span["spanID"]: span for span in spans}
            
            timeline = []
            for span in spans:
                tags = {tag["key"]: tag["value"] for tag in span.get("tags", [])}
                
                # Check for errors
                is_error = False
                error_msg = None
                if tags.get("error"):
                    is_error = True
                
                # Extract events (logs)
                events = []
                for log in span.get("logs", []):
                    log_fields = {f["key"]: f["value"] for f in log.get("fields", [])}
                    if "exception.message" in log_fields:
                        is_error = True
                        error_msg = log_fields["exception.message"]
                    events.append({
                        "timestamp": log["timestamp"],
                        "fields": log_fields
                    })
                
                start_time_us = span["startTime"]
                duration_us = span["duration"]
                
                parent_id = None
                for ref in span.get("references", []):
                    if ref["refType"] == "CHILD_OF":
                        parent_id = ref["spanID"]
                        
                timeline.append({
                    "span_id": span["spanID"],
                    "parent_id": parent_id,
                    "operation_name": span["operationName"],
                    "service_name": processes.get(span["processID"], {}).get("serviceName", "unknown"),
                    "start_time": start_time_us,
                    "duration_ms": duration_us / 1000.0,
                    "tags": tags,
                    "events": events,
                    "is_error": is_error,
                    "error_message": error_msg
                })
                
            # Sort chronologically
            timeline.sort(key=lambda x: x["start_time"])
            
            return {
                "trace_id": trace_id,
                "spans": timeline
            }
            
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Failed to connect to Jaeger: {str(e)}")
