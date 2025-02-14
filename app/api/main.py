from fastapi import APIRouter

from app.api.routers import *

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"], prefix="/auth")
api_router.include_router(user_router, tags=["users"], prefix="/users")
api_router.include_router(flower_router, tags=["flowers"], prefix="/flowers")
api_router.include_router(personal_flower_router, tags=["personal_flowers"], prefix="/personal_flowers")
api_router.include_router(message_router, tags=["messages"], prefix="/messages")
api_router.include_router(review_router, tags=["reviews"], prefix="/reviews")
api_router.include_router(advice_router, tags=["advices"], prefix="/advices")
