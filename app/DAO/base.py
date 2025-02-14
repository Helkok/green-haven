from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import *
from app.utils.exceptions import BadRequestError


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

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        '''Функция для добавления объекта в базу данных'''
        new_model = cls.model(**values)
        session.add(new_model)
        await session.commit()
        return new_model

    @classmethod
    async def delete(cls, session: AsyncSession, data_id: int):
        query = await session.execute(select(cls.model).filter_by(id=data_id))
        result = query.scalar_one_or_none()
        if result is None:
            raise BadRequestError
        try:
            await session.delete(result)
            await session.commit()
            return f"Успешный ответ."
        except Exception as e:
            await session.rollback()
            raise BadRequestError

class UserDAO(BaseDAO):
    model = User


class FlowerDAO(BaseDAO):
    model = Flower


class PersonalFlowerDAO(BaseDAO):
    model = PersonalFlower


class MessageDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, user_id_1, user_id_2, session: AsyncSession):
        '''Функция для получения сообщений между пользователями'''
        result = await session.execute(select(Message).filter(
            ((Message.user_from == user_id_1) & (Message.user_to == user_id_2)) |
            ((Message.user_from == user_id_2) & (Message.user_to == user_id_1))
        ))
        return result.scalars().all()


