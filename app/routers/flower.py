from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from app.schemas.flower import FlowerCreate
from app.utils.flowers import get_all_flowers_from_db, add_flower_to_db

router = APIRouter()




@router.get("/get_all_flower/", summary="Получить список всех цветов")
async def get_all_flowers(request: Request):
    all_flowers = await get_all_flowers_from_db(request.state.db)
    return all_flowers





@router.post("/add_flower/", summary="Добавить новый цветок")
async def add_flower(flower: FlowerCreate, request: Request):
    new_flower = await add_flower_to_db(flower, request.state.db)
    return f"Цветок {new_flower.name} успешно добавлен в базу данных"