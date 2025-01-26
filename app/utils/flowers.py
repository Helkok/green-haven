from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Flower
from app.schemas.flower import FlowerCreate


async def get_all_flowers_from_db(session: AsyncSession):
    result = await session.execute(select(Flower))
    flowers = result.scalars().all()
    return flowers

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