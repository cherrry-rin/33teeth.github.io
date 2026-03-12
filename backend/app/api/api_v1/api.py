from fastapi import APIRouter

from app.api.api_v1.endpoints import feedback, subscriber

api_router = APIRouter()
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(subscriber.router, prefix="/subscriber", tags=["subscriber"])