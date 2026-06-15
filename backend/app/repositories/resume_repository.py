"""Data access for resumes."""
from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Resume, session)

    async def list_for_user(
        self,
        user_id: uuid.UUID,
        *,
        offset: int,
        limit: int,
        search: str | None = None,
    ) -> tuple[list[Resume], int]:
        conditions = [Resume.user_id == user_id]
        if search:
            conditions.append(Resume.file_name.ilike(f"%{search}%"))

        base = select(Resume).where(*conditions)
        total = await self.session.scalar(
            select(func.count()).select_from(base.subquery())
        )
        stmt = base.order_by(Resume.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), int(total or 0)

    async def get_owned(self, resume_id: uuid.UUID, user_id: uuid.UUID) -> Resume | None:
        return await self.get_by(id=resume_id, user_id=user_id)

    async def next_version(self, user_id: uuid.UUID, file_name: str) -> int:
        stmt = select(func.coalesce(func.max(Resume.version), 0)).where(
            Resume.user_id == user_id, Resume.file_name == file_name
        )
        current = await self.session.scalar(stmt)
        return int(current or 0) + 1

    async def clear_primary(self, user_id: uuid.UUID) -> None:
        await self.session.execute(
            update(Resume).where(Resume.user_id == user_id).values(is_primary=False)
        )
