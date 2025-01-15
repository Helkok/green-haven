from app.core.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.personal_flower import PersonalFlower
from app.models.type_note import TypeNote


class Note(Base):
    """Таблица notes содержит информацию о заметках."""
    __tablename__ = "notes"

    personal_flower_id: Mapped[int] = mapped_column(ForeignKey("personal_flowers.id"), nullable=False)
    type_note_id: Mapped[int] = mapped_column(ForeignKey("type_notes.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(300), nullable=False)
    photo: Mapped[str | None] = mapped_column(String(150))

    personal_flower: Mapped["PersonalFlower"] = relationship("PersonalFlower", back_populates="notes")
    type_note: Mapped["TypeNote"] = relationship("TypeNote", back_populates="notes")
