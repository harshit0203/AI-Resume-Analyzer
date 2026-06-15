from __future__ import annotations

from datetime import datetime
from math import ceil
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

class ORMModel(BaseModel):

    model_config = ConfigDict(from_attributes=True)

class APIResponse(BaseModel, Generic[T]):

    success: bool = True
    data: T | None = None
    message: str | None = None

class MessageResponse(BaseModel):
    success: bool = True
    message: str

class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

class Page(BaseModel, Generic[T]):

    success: bool = True
    items: list[T]
    meta: PageMeta

    @classmethod
    def create(cls, items: list[T], total: int, page: int, page_size: int) -> "Page[T]":
        total_pages = ceil(total / page_size) if page_size else 0
        return cls(
            items=items,
            meta=PageMeta(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            ),
        )

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: str | None = None
    sort_by: str | None = None
    sort_order: Literal["asc", "desc"] = "desc"

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
