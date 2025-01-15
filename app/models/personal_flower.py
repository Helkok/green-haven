from datetime import timedelta

from app.core.database import Base
from sqlalchemy import String, ForeignKey, Boolean, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PersonalFlower(Base):
    """Таблица personal_flowers содержит персональные цветы пользователей"""

    __tablename__ = "personal_flowers"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=True)
    photo: Mapped[str] = mapped_column(String(150), nullable=True)
    room: Mapped[str] = mapped_column(String(15), nullable=True)
    for_trade: Mapped[bool] = mapped_column(Boolean, default=False)
    watering_interval: Mapped[timedelta | None] = mapped_column(Interval)  # Интервал полива
    fertilizing_interval: Mapped[timedelta | None] = mapped_column(Interval)  # Интервал удобрения
    transplanting_interval: Mapped[timedelta | None] = mapped_column(Interval)  # Интервал пересадки

    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    flower = relationship("Flower", back_populates="personal_flower")
    user = relationship("User", back_populates="personal_flower")
