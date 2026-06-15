from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.models.enums import ResumeStatus
from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository
from app.services.storage_service import storage_service
from app.utils.text_extraction import extract_text

logger = get_logger(__name__)

class ResumeService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.resumes = ResumeRepository(session)

    async def upload(
        self,
        user_id: uuid.UUID,
        *,
        file_name: str,
        content_type: str,
        data: bytes,
        make_primary: bool = True,
    ) -> Resume:
        storage_service.validate(file_name, len(data))
        relative_path, checksum = await storage_service.save(user_id, file_name, data)
        version = await self.resumes.next_version(user_id, file_name)

        if make_primary:
            await self.resumes.clear_primary(user_id)

        resume = await self.resumes.create(
            user_id=user_id,
            file_name=file_name,
            storage_path=relative_path,
            content_type=content_type,
            file_size=len(data),
            checksum=checksum,
            version=version,
            is_primary=make_primary,
            status=ResumeStatus.UPLOADED,
        )

        await self._parse(resume, data, content_type, file_name)
        await self.session.refresh(resume)
        return resume

    async def _parse(
        self, resume: Resume, data: bytes, content_type: str, file_name: str
    ) -> None:
        from app.agents.parser_agent import quick_structure

        try:
            resume.status = ResumeStatus.PARSING
            await self.session.flush()
            raw_text = extract_text(data, content_type, file_name)
            structured = quick_structure(raw_text)
            resume.raw_text = raw_text
            resume.parsed_data = structured
            resume.status = ResumeStatus.PARSED
            resume.parse_error = None
        except Exception as exc:
            logger.exception("Resume parsing failed for %s", resume.id)
            resume.status = ResumeStatus.FAILED
            resume.parse_error = str(exc)
        await self.session.flush()

    async def get_owned(self, resume_id: uuid.UUID, user_id: uuid.UUID) -> Resume:
        resume = await self.resumes.get_owned(resume_id, user_id)
        if resume is None:
            raise NotFoundError("Resume not found.")
        return resume

    async def list(
        self, user_id: uuid.UUID, *, offset: int, limit: int, search: str | None
    ) -> tuple[list[Resume], int]:
        return await self.resumes.list_for_user(
            user_id, offset=offset, limit=limit, search=search
        )

    async def delete(self, resume_id: uuid.UUID, user_id: uuid.UUID) -> None:
        resume = await self.get_owned(resume_id, user_id)
        storage_service.delete(resume.storage_path)
        await self.resumes.delete(resume)

    async def set_primary(self, resume_id: uuid.UUID, user_id: uuid.UUID) -> Resume:
        resume = await self.get_owned(resume_id, user_id)
        await self.resumes.clear_primary(user_id)
        return await self.resumes.update(resume, is_primary=True)
