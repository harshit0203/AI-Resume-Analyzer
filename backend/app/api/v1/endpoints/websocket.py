from __future__ import annotations

import uuid

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from jose import JWTError

from app.core.database import AsyncSessionLocal
from app.core.logging import get_logger
from app.core.security import decode_token
from app.repositories.analysis_repository import AnalysisRepository
from app.services.realtime import connection_manager

logger = get_logger(__name__)
router = APIRouter(tags=["realtime"])

@router.websocket("/ws/analyses/{analysis_id}")
async def analysis_updates(
    websocket: WebSocket,
    analysis_id: uuid.UUID,
    token: str | None = Query(default=None),
) -> None:
    access_token = token or websocket.cookies.get("ara_access_token")
    if not access_token:
        await websocket.close(code=4401)
        return
    try:
        payload = decode_token(access_token, "access")
        user_id = uuid.UUID(payload["sub"])
    except (JWTError, KeyError, ValueError):
        await websocket.close(code=4401)
        return

    async with AsyncSessionLocal() as session:
        analysis = await AnalysisRepository(session).get(analysis_id)
        if analysis is None or analysis.user_id != user_id:
            await websocket.close(code=4403)
            return
        current_status = analysis.status.value

    await connection_manager.connect(str(analysis_id), websocket)
    await websocket.send_json({
        "type": "connected",
        "analysis_id": str(analysis_id),
        "status": current_status,
    })
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await connection_manager.disconnect(str(analysis_id), websocket)
    except Exception:
        await connection_manager.disconnect(str(analysis_id), websocket)
