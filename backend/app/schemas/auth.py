from __future__ import annotations

import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user import UserPublic

_PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$")

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not _PASSWORD_PATTERN.match(value):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter and one number."
            )
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not _PASSWORD_PATTERN.match(value):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter and one number."
            )
        return value
