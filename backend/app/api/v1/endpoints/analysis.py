"""Analysis lifecycle endpoints: create, run, list, retrieve, stats."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.database import AsyncSessionLocal
from app.core.logging import get_logger
from app.models.user import User
from app.schemas.analysis import AnalysisDetail, AnalysisListItem, CreateAnalysisRequest
from app.schemas.common import APIResponse, MessageResponse, Page
from app.services.analysis_service import AnalysisService

logger = get_logger(__name__)
router = APIRouter(prefix="/analyses", tags=["analyses"])


async def _run_analysis_task(analysis_id: uuid.UUID) -> None:
    """Background task: execute the workflow with its own DB session."""
    async with AsyncSessionLocal() as session:
        try:
            await AnalysisService(session).run(analysis_id)
            await session.commit()
        except Exception:  # pragma: no cover - defensive
            await session.rollback()
            logger.exception("Background analysis %s crashed", analysis_id)


@router.post("", response_model=APIResponse[AnalysisDetail], status_code=status.HTTP_202_ACCEPTED)
async def create_analysis(
    payload: CreateAnalysisRequest,
    background: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[AnalysisDetail]:
    service = AnalysisService(db)
    analysis = await service.create(user.id, payload.resume_id, payload.target_role)
    await db.commit()
    background.add_task(_run_analysis_task, analysis.id)
    detail = await service.get_detail(analysis.id, user.id)
    return APIResponse(
        data=AnalysisDetail.model_validate(detail),
        message="Analysis started. Connect to the WebSocket for live updates.",
    )


@router.get("", response_model=Page[AnalysisListItem])
async def list_analyses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    resume_id: uuid.UUID | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Page[AnalysisListItem]:
    offset = (page - 1) * page_size
    items, total = await AnalysisService(db).list(
        user.id, offset=offset, limit=page_size, resume_id=resume_id
    )
    return Page.create(
        [AnalysisListItem.model_validate(item) for item in items], total, page, page_size
    )


@router.get("/stats", response_model=APIResponse[dict])
async def analysis_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[dict]:
    return APIResponse(data=await AnalysisService(db).stats(user.id))


@router.get("/{analysis_id}", response_model=APIResponse[AnalysisDetail])
async def get_analysis(
    analysis_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[AnalysisDetail]:
    analysis = await AnalysisService(db).get_detail(analysis_id, user.id)
    return APIResponse(data=AnalysisDetail.model_validate(analysis))


@router.delete("/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    await AnalysisService(db).delete(analysis_id, user.id)
    return MessageResponse(message="Analysis deleted.")
