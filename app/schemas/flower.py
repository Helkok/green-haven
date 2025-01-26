from datetime import timedelta

from pydantic import BaseModel, Field


class FlowerCreate(BaseModel):
    name: str = Field(..., description="Название цветка")
    level_watering: int | None = Field(None, description="Уровень полива")
    level_lighting: int | None = Field(None, description="Уровень освещения")
    level_toxicity: int | None = Field(None, description="Уровень токсичности")
    description: str | None = Field(None, description="Описание цветка")
    photo: str | None = Field(None, description="Фото цветка")
    watering_interval: timedelta | None = Field(None, description="Интервал полива")
    fertilizing_interval: timedelta | None = Field(None, description="Интервал удобрения")
    transplanting_interval: timedelta | None = Field(None, description="Интервал пересадки")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Роза",
                "level_watering": 3,
                "level_lighting": 2,
                "level_toxicity": 1,
                "description": "Красивый цветок",
                "photo": "https://example.com/photo.jpg",
            }
        }
