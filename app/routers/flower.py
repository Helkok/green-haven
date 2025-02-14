from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

from app.DAO.base import FlowerDAO
from app.schemas.flower import FlowerCreate
from app.utils.flowers import add_flower_to_db

router = APIRouter()


@router.get("/get_flower/{flower_id}", summary="Получить информацию о цветке", response_model=FlowerCreate)
async def get_flower(flower_id: int, request: Request):
    flower = await FlowerDAO.find_one_or_none_by_id(session=request.state.db, data_id=flower_id)
    if flower is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Цветок не найден")
    return flower


@router.get("/getList/", summary="Получить список всех цветов", response_model=list[FlowerCreate])
async def get_all_flowers(request: Request):
    all_flowers = await FlowerDAO.find_all(session=request.state.db)
    return all_flowers


@router.post("/add_flower/", summary="Добавить новый цветок")
async def add_flower(flower: FlowerCreate, request: Request) -> str:
    new_flower = await add_flower_to_db(flower, request.state.db)
    return f"Цветок {new_flower.name} успешно добавлен в базу данных"


@router.delete("/delete_flower/{flower_id}", summary="Удалить цветок", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flower(flower_id: int, request: Request):
    await FlowerDAO.delete(session=request.state.db, data_id=flower_id)
