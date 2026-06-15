from __future__ import annotations

import uuid
from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, entity_id: uuid.UUID) -> ModelType | None:
        return await self.session.get(self.model, entity_id)

    async def get_by(self, **filters: Any) -> ModelType | None:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
        order_by: Any | None = None,
    ) -> Sequence[ModelType]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            stmt = stmt.order_by(self.model.created_at.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        stmt = select(func.count()).select_from(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def create(self, **values: Any) -> ModelType:
        instance = self.model(**values)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    def add(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        return instance

    async def update(self, instance: ModelType, **values: Any) -> ModelType:
        for key, value in values.items():
            setattr(instance, key, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    async def flush(self) -> None:
        await self.session.flush()
