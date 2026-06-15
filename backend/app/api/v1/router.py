"""Aggregate router for API v1."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import analysis, auth, resumes, users, websocket

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(resumes.router)
api_router.include_router(analysis.router)

# WebSocket router is mounted without the version prefix at the app level,
# but exposed here too for completeness of the v1 surface.
ws_router = websocket.router
