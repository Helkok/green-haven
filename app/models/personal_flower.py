from app.core.database import Base
from sqlalchemy import String, ForeignKey, Boolean, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.flower import Flower
from app.models.user import User


class PersonalFlower(Base):
    """Таблица personal_flowers содержит персональные цветы пользователей"""

    __tablename__ = "personal_flowers"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=True)
    photo: Mapped[str] = mapped_column(String(150), nullable=True)
    room: Mapped[str] = mapped_column(String(15), nullable=True)
    for_trade: Mapped[bool] = mapped_column(Boolean, default=False)
    watering_interval: Mapped[Interval] = mapped_column(Interval, nullable=True)  # Интервал полива
    fertilizing_interval: Mapped[Interval] = mapped_column(Interval, nullable=True)  # Интервал удобрения
    transplanting_interval: Mapped[Interval] = mapped_column(Interval, nullable=True)  # Интервал пересадки

    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    flower: Mapped["Flower"] = relationship("Flower", back_populates="personal_flower")
    user: Mapped["User"] = relationship("User", back_populates="personal_flower")
