from fastapi import APIRouter, Request

from app.DAO.base import UserDAO
from app.api.dependencies import current_user
from app.schemas.user import UserEdit, UserResponse
from app.utils.exceptions import BadRequestError

router = APIRouter()


@router.get("/get_me/", summary="Получить информацию о текущем пользователе")
async def get_me(user: current_user) -> UserResponse:
    return user


@router.patch("/edit_me/", summary="Изменить информацию о текущем пользователе")
async def edit_me(filters: UserEdit, request: Request, user: current_user) -> UserResponse:
    db_user = await UserDAO.edit_user(user_id=user.id, session=request.state.db, **filters.model_dump())
    return db_user


@router.get("/get_user/{user_id}", summary="Получить информацию о пользователе по ID")
async def get_user(user_id: int, request: Request, user: current_user) -> UserResponse:
    db_user = await UserDAO.find_one_or_none_by_id(data_id=user_id, session=request.state.db)
    if db_user is None:
        raise BadRequestError(detail="Пользователь не найден")
    return db_user


@router.delete("/delete_me/}", summary="Удалить профиль")
async def delete_me(user: current_user, request: Request):
    await UserDAO.delete(session=request.state.db, data_id=user.id)
    return {"message": "Профиль успешно удален"}
