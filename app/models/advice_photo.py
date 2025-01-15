from app.core.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.advice import Advice


class AdvicePhoto(Base):
    """Таблица advice_photos содержит информацию о фотографиях советов."""
    __tablename__ = "advice_photos"

    advice_id: Mapped[int] = mapped_column(ForeignKey("advices.id"), nullable=False)
    photo: Mapped[str] = mapped_column(String(150), nullable=False)

    advice: Mapped["Advice"] = relationship("Advice", back_populates="advice_photos")