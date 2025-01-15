from app.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship



class TypeNote(Base):
    """Таблица type_notes содержит информацию о типах заметок."""
    __tablename__ = "type_notes"


    name: Mapped[str] = mapped_column(String(20), nullable=False)

    notes = relationship("Note", back_populates="type_note", cascade="all, delete-orphan")
