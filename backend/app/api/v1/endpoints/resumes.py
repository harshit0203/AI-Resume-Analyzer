from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import APIResponse, MessageResponse, Page
from app.schemas.resume import ResumeListItem, ResumePublic
from app.services.resume_service import ResumeService
from app.services.storage_service import storage_service

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("", response_model=APIResponse[ResumePublic], status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[ResumePublic]:
    data = await file.read()
    resume = await ResumeService(db).upload(
        user.id,
        file_name=file.filename or "resume.pdf",
        content_type=file.content_type or "application/octet-stream",
        data=data,
    )
    return APIResponse(data=ResumePublic.model_validate(resume), message="Resume uploaded and parsed.")

@router.get("", response_model=Page[ResumeListItem])
async def list_resumes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Page[ResumeListItem]:
    offset = (page - 1) * page_size
    items, total = await ResumeService(db).list(user.id, offset=offset, limit=page_size, search=search)
    return Page.create(
        [ResumeListItem.model_validate(item) for item in items], total, page, page_size
    )

@router.get("/{resume_id}", response_model=APIResponse[ResumePublic])
async def get_resume(
    resume_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[ResumePublic]:
    resume = await ResumeService(db).get_owned(resume_id, user.id)
    return APIResponse(data=ResumePublic.model_validate(resume))

@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    resume = await ResumeService(db).get_owned(resume_id, user.id)
    data = await storage_service.read(resume.storage_path)
    return StreamingResponse(
        iter([data]),
        media_type=resume.content_type,
        headers={"Content-Disposition": f'attachment; filename="{resume.file_name}"'},
    )

@router.post("/{resume_id}/primary", response_model=APIResponse[ResumePublic])
async def set_primary(
    resume_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[ResumePublic]:
    resume = await ResumeService(db).set_primary(resume_id, user.id)
    return APIResponse(data=ResumePublic.model_validate(resume), message="Primary resume updated.")

@router.delete("/{resume_id}", response_model=MessageResponse)
async def delete_resume(
    resume_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    await ResumeService(db).delete(resume_id, user.id)
    return MessageResponse(message="Resume deleted.")
