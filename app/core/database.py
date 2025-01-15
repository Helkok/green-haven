from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from config import settings
from app.utils.base import created_at, updated_at, int_pk

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, )

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
