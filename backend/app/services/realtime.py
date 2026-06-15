"""In-process WebSocket connection manager for live analysis updates.

Connections are keyed by ``analysis_id`` so multiple browser tabs watching the
same analysis all receive the agent lifecycle events.
"""
from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any

from fastapi import WebSocket

from app.core.logging import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, analysis_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections[analysis_id].add(websocket)
        logger.info("WebSocket connected for analysis %s", analysis_id)

    async def disconnect(self, analysis_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections[analysis_id].discard(websocket)
            if not self._connections[analysis_id]:
                self._connections.pop(analysis_id, None)

    async def broadcast(self, analysis_id: str, message: dict[str, Any]) -> None:
        targets = list(self._connections.get(analysis_id, set()))
        dead: list[WebSocket] = []
        for ws in targets:
            try:
                await ws.send_json(message)
            except Exception:  # pragma: no cover - client disconnected
                dead.append(ws)
        for ws in dead:
            await self.disconnect(analysis_id, ws)


connection_manager = ConnectionManager()
