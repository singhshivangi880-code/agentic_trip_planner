from fastapi import APIRouter
from app.api.v1 import trips
from app.api.v1 import decisions
from app.api.v1 import workflow
from app.api.v1 import share
from app.api.v1 import dev
from app.api.v1 import chat

api_router = APIRouter()
api_router.include_router(trips.router)
api_router.include_router(decisions.router)
api_router.include_router(workflow.router)
api_router.include_router(share.router, prefix="/share", tags=["share"])
api_router.include_router(dev.router)
api_router.include_router(chat.router)

@api_router.get("/ping")
async def ping():
    return {"ping": "pong"}
