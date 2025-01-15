from app.core.database import Base
from pydantic import EmailStr
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class Message(Base):
    """Таблица messages содержит сообщения между пользователями."""
    __tablename__ = "messages"

    user_from: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_to: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    def set_message(self, message: str):
        """Шифрует сообщение перед сохранением в базе данных."""
        self.message = cipher_suite.encrypt(message.encode()).decode()

    def get_message(self):
        """Дешифрует сообщение при извлечении из базы данных."""
        return cipher_suite.decrypt(self.message.encode()).decode()
