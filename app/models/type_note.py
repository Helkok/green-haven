from app.core.database import Base
from pydantic import EmailStr
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.note import Note


class TypeNote(Base):
    """Таблица type_notes содержит информацию о типах заметок."""
    __tablename__ = "type_notes"


    name: Mapped[str] = mapped_column(String(20), nullable=False)

    notes: Mapped[list["Note"]] = relationship("Note", back_populates="type_note", cascade="all, delete-orphan")
