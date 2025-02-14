from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Flower
from app.schemas.flower import FlowerCreate


async def delete_flower_from_db(flower_id: int, session: AsyncSession) -> str:
    db_flower = await session.execute(select(Flower).filter_by(id=flower_id))
    db_flower = db_flower.scalar_one_or_none()
    if db_flower is None:
        raise Exception(f"Цветок с id {flower_id} не найден")
    try:
        await session.delete(db_flower)
        await session.commit()
        return f"{db_flower.name} успешно удален из базы данных"
    except Exception as e:
        await session.rollback()
        raise e


async def add_flower_to_db(flower: FlowerCreate, session: AsyncSession) -> Flower:
    db_flower = Flower(
        name=flower.name,
        level_watering=flower.level_watering,
        level_lighting=flower.level_lighting,
        level_toxicity=flower.level_toxicity,
        description=flower.description,
        photo=flower.photo,
        watering_interval=flower.watering_interval,
        fertilizing_interval=flower.fertilizing_interval,
        transplanting_interval=flower.transplanting_interval
    )
    try:
        session.add(db_flower)
        await session.commit()
        await session.refresh(db_flower)
        return db_flower
    except Exception as e:
        await session.rollback()
        raise e
