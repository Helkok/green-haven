from datetime import timedelta, datetime

from app.core.database import Base
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SessionTable(Base):
    """Сессия пользователя"""
    __tablename__ = "sessions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    user_agent: Mapped[str | None]
    ip_address: Mapped[str | None]
    expired_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    user = relationship("User", back_populates="session")

    def __repr__(self):
        return f"<Session {self.id}>"
