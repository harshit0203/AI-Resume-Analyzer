from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from argon2 import PasswordHasher
from argon2 import exceptions as argon2_exceptions
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import UnauthorizedError

TokenType = Literal["access", "refresh"]

_password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)

def hash_password(password: str) -> str:
    return _password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        return _verify_bcrypt(plain_password, hashed_password)
    try:
        return _password_hasher.verify(hashed_password, plain_password)
    except (
        argon2_exceptions.VerifyMismatchError,
        argon2_exceptions.VerificationError,
        argon2_exceptions.InvalidHashError,
    ):
        return False

def needs_rehash(hashed_password: str) -> bool:
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        return True
    try:
        return _password_hasher.check_needs_rehash(hashed_password)
    except argon2_exceptions.InvalidHashError:
        return True

def _verify_bcrypt(plain_password: str, hashed_password: str) -> bool:
    try:
        import bcrypt

        pw = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pw, hashed_password.encode("utf-8"))
    except Exception:
        return False

def _create_token(
    subject: str,
    token_type: TokenType,
    expires_delta: timedelta,
    secret: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "jti": str(uuid.uuid4()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM)

def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    return _create_token(
        subject,
        "access",
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        settings.JWT_SECRET_KEY,
        extra_claims,
    )

def create_refresh_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    return _create_token(
        subject,
        "refresh",
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        settings.JWT_REFRESH_SECRET_KEY,
        extra_claims,
    )

def decode_token(token: str, token_type: TokenType) -> dict[str, Any]:
    secret = settings.JWT_SECRET_KEY if token_type == "access" else settings.JWT_REFRESH_SECRET_KEY
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise UnauthorizedError("Invalid or expired token.") from exc
    if payload.get("type") != token_type:
        raise UnauthorizedError("Incorrect token type.")
    return payload
