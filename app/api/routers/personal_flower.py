from fastapi import APIRouter
from starlette.requests import Request

from app.DAO.base import PersonalFlowerDAO
from app.api.dependencies import current_user

router = APIRouter()


@router.get("/get_flower/{user_id}", summary="Получить список всех цветов пользователя")
async def get_all_flowers(user_id: int, request: Request, user: current_user):
    all_personal_flowers = await PersonalFlowerDAO.find_all_by_filters(session=request.state.db, user_id=user_id)
    return all_personal_flowers


@router.get("/get_flower/{flower_id}", summary="Получить информацию о персональном цветке")
async def get_flower(flower_id: int, request: Request):
    pass


@router.get("/all_trades/", summary="Получить список всех обменов")
async def get_all_trades(request: Request):
    pass


@router.post("/add_flower/", summary="Добавить новый персональный цветок")
async def add_flower(request: Request, user: current_user):
    pass


@router.post("/trade_flower/", summary="Обменять персональный цветок")
async def trade_flower(request: Request, user: current_user):
    pass


@router.patch("/update_flower/{flower_id}", summary="Обновить персональный цветок")
async def update_flower(flower_id: int, request: Request):
    pass


@router.delete("/delete_flower/{flower_id}", summary="Удалить персональный цветок")
async def delete_flower(flower_id: int, request: Request):
    pass
