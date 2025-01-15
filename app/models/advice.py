from app.core.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Advice(Base):
    """Таблица advice содержит информацию о советах."""
    __tablename__ = "advices"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(300), nullable=False)

    user = relationship("User", back_populates="advices")
    flower = relationship("Flower", back_populates="advices")
    advice_photos = relationship("AdvicePhoto", back_populates="advice", cascade="all, delete-orphan")
