from datetime import timedelta

from app.core.database import Base
from sqlalchemy import String, ForeignKey, Interval, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Flower(Base):
    """Таблица flowers содержит информацию о цветах."""
    __tablename__ = "flowers"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    level_watering: Mapped[int | None]
    level_lighting: Mapped[int | None]
    level_toxicity: Mapped[int | None]

    description: Mapped[str | None] = mapped_column(String(300))
    photo: Mapped[str | None] = mapped_column(String(150))

    watering_interval: Mapped[timedelta | None]  # Интервал полива
    fertilizing_interval: Mapped[timedelta | None]  # Интервал удобрения
    transplanting_interval: Mapped[timedelta | None]  # Интервал пересадки

    reviews = relationship("Review", back_populates="flower")
    personal_flower = relationship("PersonalFlower", back_populates="flower")
    advices = relationship("Advice", back_populates="flower")
