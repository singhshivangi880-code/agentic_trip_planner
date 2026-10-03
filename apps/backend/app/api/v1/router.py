from fastapi import APIRouter
from app.api.v1 import trips

api_router = APIRouter()
api_router.include_router(trips.router)

@api_router.get("/ping")
async def ping():
    return {"ping": "pong"}
