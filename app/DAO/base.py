from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import *


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_filters(cls, session: AsyncSession, **filters):
        '''Функция для поиска одного объекта по фильтрам'''
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, filters=None):
        '''Функция для поиска всех объектов'''
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def find_all_by_filters(cls, session: AsyncSession, **filters):
        '''Функция для поиска всех объектов по фильтрам'''
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        '''Функция для поиска одного объекта по id'''
        result = await session.execute(select(cls.model).filter_by(id=data_id))
        return result.scalar_one_or_none()


class UserDAO(BaseDAO):
    model = User


class FlowerDAO(BaseDAO):
    model = Flower

    @classmethod
    async def delete(cls, session: AsyncSession, data_id: int):
        '''Функция для удаления цветка из базы данных'''
        result = await session.execute(select(Flower).filter_by(id=data_id))
        db_flower = result.scalar_one_or_none()
        if db_flower is None:
            raise Exception(f"Цветок с id {data_id} не найден")
        try:
            await session.delete(db_flower)
            await session.commit()
            return f"{db_flower.name} успешно удален из базы данных"
        except Exception as e:
            await session.rollback()
            raise e


class PersonalFlowerDAO(BaseDAO):
    model = PersonalFlower
