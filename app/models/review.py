from app.core.database import Base
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Review(Base):
    """Таблица reviews содержит информацию о отзывах."""
    __tablename__ = "reviews"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    flower_id: Mapped[int] = mapped_column(ForeignKey("flowers.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String(300), nullable=False)

    user = relationship("User", back_populates="reviews")
    flower = relationship("Flower", back_populates="reviews")
    review_photos = relationship("ReviewPhoto", back_populates="review", cascade="all, delete-orphan")
