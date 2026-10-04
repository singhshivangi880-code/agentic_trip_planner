from sqlalchemy import text
from app.core.config import settings
from app.core.db import get_engine


def check_database() -> str:
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception as exc:  # noqa: BLE001 - report any failure as unhealthy
        return f"error: {type(exc).__name__}"


def check_redis() -> str:
    try:
        import redis

        client = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=2, socket_timeout=2)
        client.ping()
        return "ok"
    except Exception as exc:  # noqa: BLE001
        return f"error: {type(exc).__name__}"


def check_dependencies() -> dict[str, str]:
    return {"database": check_database(), "redis": check_redis()}
