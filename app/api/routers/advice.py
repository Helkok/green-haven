from fastapi import APIRouter, Request
from sqlalchemy import select

from app.api.dependencies import current_user
from app.models import Advice, AdvicePhoto
from app.schemas.advice import AdviceCreate

router = APIRouter()


@router.get('/get_advices{flower_id}', summary='Получить советы о цветке')
async def get_reviews(flower_id: int, request: Request, user: current_user):
    advices = await request.state.db.execute(
        select(Advice).filter(Advice.flower_id == flower_id)
    )
    advices = advices.scalars().all()

    return advices


@router.post('/add_advice', summary='Добавить совет')
async def add_review(advice: AdviceCreate, request: Request, user: current_user):
    db_advice = Advice(
        user_id=advice.user_id,
        flower_id=advice.flower_id,
        text=advice.text
    )
    if advice.photo:
        db_photo_advice = AdvicePhoto(
            advice_id=db_advice.id,
            photo=advice.photo
        )
        request.state.db.add(db_photo_advice)

    request.state.db.add(db_advice)
    await request.state.db.commit()

    return {"message": "Совет успешно добавлен", "advice": db_advice.text}


@router.patch('/update_advice/{advice_id}', summary='Обновить совет')
async def update_review(advice_id: int, request: Request, user: current_user):
    pass


@router.delete('/delete_advice/{advice_id}', summary='Удалить совет')
async def delete_review(advice_id: int, request: Request, user: current_user):
    pass
