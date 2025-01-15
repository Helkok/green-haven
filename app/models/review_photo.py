from app.core.database import Base
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.review import Review

class ReviewPhoto(Base):
    """Таблица review_photos содержит информацию о фотографиях отзывов."""
    __tablename__ = "review_photos"

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=False)
    photo: Mapped[str] = mapped_column(String(150), nullable=False)

    review: Mapped["Review"] = relationship("Review", back_populates="review_photos")