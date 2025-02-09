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


class MessageDAO(BaseDAO):
    model = Message

    @classmethod
    async def add(cls, user_from, user_to, message, session: AsyncSession):
        '''Функция для добавления сообщения в базу данных'''
        try:
            new_message = Message(user_from=user_from, user_to=user_to, message=message)
            session.add(new_message)
            await session.commit()
            return new_message
        except Exception as e:
            await session.rollback()
            raise e

    @classmethod
    async def get_messages_between_users(cls, user_id_1, user_id_2, session: AsyncSession):
        '''Функция для получения сообщений между пользователями'''
        result = await session.execute(select(Message).filter(
            ((Message.user_from == user_id_1) & (Message.user_to == user_id_2)) |
            ((Message.user_from == user_id_2) & (Message.user_to == user_id_1))
        ))
        return result.scalars().all()


