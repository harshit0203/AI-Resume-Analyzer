from __future__ import annotations

from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cookies import (
    REFRESH_COOKIE,
    clear_auth_cookies,
    set_access_cookie,
    set_auth_cookies,
)
from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshResponse,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.common import APIResponse, MessageResponse
from app.schemas.user import UserPublic
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[TokenResponse]:
    service = AuthService(db)
    user = await service.register(payload)
    access, refresh = service.issue_tokens(user)
    set_auth_cookies(response, access, refresh)
    return APIResponse(
        data=TokenResponse(
            access_token=access,
            expires_in=service.access_token_max_age(),
            user=UserPublic.model_validate(user),
        ),
        message="Account created successfully.",
    )

@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[TokenResponse]:
    service = AuthService(db)
    user = await service.authenticate(payload)
    access, refresh = service.issue_tokens(user)
    set_auth_cookies(response, access, refresh)
    return APIResponse(
        data=TokenResponse(
            access_token=access,
            expires_in=service.access_token_max_age(),
            user=UserPublic.model_validate(user),
        ),
        message="Signed in successfully.",
    )

@router.post("/refresh", response_model=APIResponse[RefreshResponse])
async def refresh_token(
    response: Response,
    db: AsyncSession = Depends(get_db),
    refresh_cookie: str | None = Cookie(default=None, alias=REFRESH_COOKIE),
) -> APIResponse[RefreshResponse]:
    if not refresh_cookie:
        raise UnauthorizedError("No refresh token provided.")
    service = AuthService(db)
    _, access = await service.refresh(refresh_cookie)
    set_access_cookie(response, access)
    return APIResponse(
        data=RefreshResponse(access_token=access, expires_in=service.access_token_max_age()),
        message="Token refreshed.",
    )

@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response) -> MessageResponse:
    clear_auth_cookies(response)
    return MessageResponse(message="Signed out successfully.")

@router.get("/me", response_model=APIResponse[UserPublic])
async def me(user: User = Depends(get_current_user)) -> APIResponse[UserPublic]:
    return APIResponse(data=UserPublic.model_validate(user))
