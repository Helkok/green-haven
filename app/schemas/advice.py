from typing import List

from pydantic import BaseModel, Field


class AdviceCreate(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    flower_id: int = Field(..., description="ID цветка")
    text: str = Field(..., description="Текст совета")
    photo: List[str] | None = Field(..., description="Фотографии совета")
