from app.core.database import Base
from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


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

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    personal_flower = relationship("Flower", back_populates="user", cascade="all, delete-orphan")
    advices = relationship("Advice", back_populates="user", cascade="all, delete-orphan")
    session = relationship("SessionTable", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"
