from fastapi import Request, HTTPException, Depends
import time
from app.core.redis import redis_client

class RateLimiter:
    def __init__(self, times: int, seconds: int):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        import os
        if not redis_client or os.getenv("TESTING") == "1":
            return  # skip if redis is not available or in testing
        
        # Use client IP as identifier for now
        identifier = request.client.host if request.client else "unknown"
        key = f"rate_limit:{request.url.path}:{identifier}"
        
        current = await redis_client.get(key)
        if current and int(current) >= self.times:
            raise HTTPException(status_code=429, detail="Too Many Requests")
            
        pipeline = redis_client.pipeline()
        pipeline.incr(key)
        if not current:
            pipeline.expire(key, self.seconds)
        await pipeline.execute()

def rate_limit(times: int, seconds: int):
    return Depends(RateLimiter(times, seconds))
