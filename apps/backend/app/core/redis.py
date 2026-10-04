import json
from typing import Any, Optional
import redis.asyncio as redis
from app.core.config import settings

# ponytail: global redis client, connection pool is managed by redis-py automatically.
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class Cache:
    """Simple Redis cache abstraction."""
    
    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        val = await redis_client.get(key)
        if val is not None:
            try:
                return json.loads(val)
            except json.JSONDecodeError:
                return val
        return None

    @classmethod
    async def set(cls, key: str, value: Any, ttl: Optional[int] = None) -> None:
        val = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        await redis_client.set(key, val, ex=ttl)

    @classmethod
    async def delete(cls, key: str) -> None:
        await redis_client.delete(key)
        
    @classmethod
    async def set_workflow_state(cls, workflow_id: str, state: dict, ttl: int = 86400) -> None:
        await cls.set(f"workflow:{workflow_id}", state, ttl=ttl)
        
    @classmethod
    async def get_workflow_state(cls, workflow_id: str) -> Optional[dict]:
        return await cls.get(f"workflow:{workflow_id}")

    @classmethod
    async def check_idempotency(cls, key: str, ttl: int = 3600) -> bool:
        """Returns True if this is a new request, False if it was already processed."""
        # SET NX ensures atomic check-and-set
        return bool(await redis_client.set(f"idempotency:{key}", "1", nx=True, ex=ttl))
