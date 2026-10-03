from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

HTTP_STATUS_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMITED",
    500: "INTERNAL_SERVER_ERROR",
    503: "SERVICE_UNAVAILABLE",
}


class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: list = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []


def error_response(request: Request, status_code: int, code: str, message: str, details: list | None = None) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
                "details": details or [],
            }
        },
    )


async def app_exception_handler(request: Request, exc: AppException):
    return error_response(request, exc.status_code, exc.code, exc.message, exc.details)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        {"field": ".".join(str(p) for p in err.get("loc", [])), "message": err.get("msg"), "type": err.get("type")}
        for err in jsonable_encoder(exc.errors())
    ]
    return error_response(request, 422, "VALIDATION_ERROR", "Invalid request", details)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code = HTTP_STATUS_CODES.get(exc.status_code, "HTTP_ERROR")
    message = exc.detail if isinstance(exc.detail, str) else code.replace("_", " ").capitalize()
    return error_response(request, exc.status_code, code, message)


async def generic_exception_handler(request: Request, exc: Exception):
    return error_response(request, 500, "INTERNAL_SERVER_ERROR", "An unexpected error occurred.")


def register_exception_handlers(app) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
