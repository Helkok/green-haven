from app.core.database import Base
from sqlalchemy import String, ForeignKey, Interval, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.advice import Advice
from app.models.personal_flower import PersonalFlower
from app.models.review import Review


class Flower(Base):
    """Таблица flowers содержит информацию о цветах."""
    __tablename__ = "flowers"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    level_watering: Mapped[int | None]
    level_lighting: Mapped[int | None]
    level_toxicity: Mapped[int | None]

    description: Mapped[str | None] = mapped_column(String(300))
    photo: Mapped[str | None] = mapped_column(String(150))

    watering_interval: Mapped[Interval | None]  # Интервал полива
    fertilizing_interval: Mapped[Interval | None]  # Интервал удобрения
    transplanting_interval: Mapped[Interval | None]  # Интервал пересадки

    reviews: Mapped["Review"] = relationship("Review", back_populates="flower")
    personal_flower: Mapped["PersonalFlower"] = relationship("PersonalFlower", back_populates="flower")
    advices: Mapped["Advice"] = relationship("Advice", back_populates="flower")
