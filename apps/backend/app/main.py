from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging, log_requests_middleware
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.api.v1.router import api_router

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.middleware("http")(log_requests_middleware)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(api_router, prefix=settings.API_V1_STR)
