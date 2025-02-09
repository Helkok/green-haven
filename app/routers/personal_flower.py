

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from app.DAO.base import PersonalFlowerDAO
from app.schemas.flower import FlowerCreate
router = APIRouter()


@router.get("/get_all/", summary="Получить список всех цветов пользователя")
async def get_all_flowers(request: Request):
    all_personal_flowers = await PersonalFlowerDAO.find_all(session=request.state.db)
    return all_personal_flowers
