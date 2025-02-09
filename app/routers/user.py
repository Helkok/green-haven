from fastapi import APIRouter, Depends, Request

from app.DAO.base import UserDAO
from app.schemas.user import UserResponse
from app.utils.user import get_current_user, current_user

router = APIRouter()


@router.get("/get_me/", summary="Получить информацию о текущем пользователе")
async def get_me(user: current_user) -> UserResponse:
    return user


@router.get("/get_user/{user_id}", summary="Получить информацию о пользователе по ID")
async def get_user(user_id: int, request: Request, user: current_user) -> UserResponse:
    db_user = await UserDAO.find_one_or_none_by_id(data_id=user_id, session=request.state.db)
    return db_user
