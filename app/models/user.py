from app.core.database import Base
from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.advice import Advice
from app.models.personal_flower import PersonalFlower
from app.models.review import Review


class User(Base):
    """Таблица users содержит информацию о пользователях."""
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[EmailStr] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    info: Mapped[str] = mapped_column(String(150), nullable=False)
    photo: Mapped[str | None] = mapped_column(String(150))

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    personal_flower: Mapped[list["PersonalFlower"]] = relationship("Flower", back_populates="user", cascade="all, delete-orphan")
    advices: Mapped[list["Advice"]] = relationship("Advice", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"
