from fastapi import APIRouter, Request
from sqlalchemy import select

from app.api.dependencies import current_user
from app.models import Review
from app.schemas.review import ReviewCreate
from app.utils.exceptions import BadRequestError

router = APIRouter()


@router.get('/get_reviews{flower_id}', summary='Получить отзывы о цветке')
async def get_reviews(flower_id: int, request: Request, user: current_user):
    reviews = await request.state.db.execute(
        select(Review).filter(Review.flower_id == flower_id)
    )
    reviews = reviews.scalars().all()

    return reviews


@router.post('/add_review', summary='Добавить отзыв')
async def add_review(review: ReviewCreate, request: Request, user: current_user):
    existing_review = await request.state.db.execute(
        select(Review).filter(
            Review.user_id == review.user_id,
            Review.flower_id == review.flower_id
        )
    )
    existing_review = existing_review.scalars().first()

    if existing_review:
        raise BadRequestError(detail="Вы уже оставили отзыв для этого цветка.")

    db_review = Review(
        user_id=review.user_id,
        flower_id=review.flower_id,
        rating=review.rating,
        text=review.text
    )

    request.state.db.add(db_review)
    await request.state.db.commit()

    return {"message": "Отзыв успешно добавлен", "review": db_review.text}


@router.patch('/update_review/{review_id}', summary='Обновить отзыв')
async def update_review(review_id: int, request: Request, user: current_user):
    pass


@router.delete('/delete_review/{review_id}', summary='Удалить отзыв')
async def delete_review(review_id: int, request: Request, user: current_user):
    pass
