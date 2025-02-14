from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    flower_id: int = Field(..., description="ID цветка")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг от 1 до 5")
    text: str = Field(..., description="Текст отзыва")
