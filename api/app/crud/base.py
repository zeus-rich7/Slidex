from datetime import datetime
from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, inspect

from app import dto
from app.models import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        def to_dict(obj):
            result = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
            # Convert datetime to string
            for key, value in result.items():
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
            return result
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return [to_dict(template) for template in result.scalars().all()]

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        obj = self.model(**obj_in)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, id: int, obj_in: dict) -> ModelType | None:
        obj = await self.get(db, id)
        if not obj:
            return None
        for field, value in obj_in.items():
            setattr(obj, field, value)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        obj = await self.get(db, id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True