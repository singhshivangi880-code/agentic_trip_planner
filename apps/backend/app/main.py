from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.core.config import settings
from app.core.logging import setup_logging, log_requests_middleware
from app.core.exceptions import register_exception_handlers
from app.core.health import check_dependencies
from app.api.v1.router import api_router

# Try to initialize tracing from our common package
try:
    from agents.common.tracing.setup import init_tracing
    init_tracing(service_name="trip_planner_backend")
except ImportError:
    pass

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

FastAPIInstrumentor.instrument_app(app)

app.middleware("http")(log_requests_middleware)

register_exception_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready():
    """Readiness probe: verifies connectivity to PostgreSQL and Redis (Connectivity Check C2)."""
    checks = check_dependencies()
    ok = all(c == "ok" for c in checks.values())
    return JSONResponse(status_code=200 if ok else 503, content={"status": "ok" if ok else "degraded", "checks": checks})


app.include_router(api_router, prefix=settings.API_V1_STR)
