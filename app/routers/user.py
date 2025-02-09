from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.utils.user import get_current_user, current_user

router = APIRouter()


@router.get("/get_me/", response_model=UserResponse, summary="Получить информацию о текущем пользователе")
async def get_me(user: current_user):
    return user

