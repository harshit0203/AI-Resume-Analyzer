from __future__ import annotations

import hashlib
import uuid
from pathlib import Path

import aiofiles

from app.core.config import settings
from app.core.exceptions import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)

class StorageService:

    def __init__(self) -> None:
        self.base_dir = Path(settings.UPLOAD_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def validate(self, file_name: str, size: int) -> None:
        suffix = Path(file_name).suffix.lower()
        if suffix not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            raise ValidationError(
                f"File type '{suffix}' is not allowed. "
                f"Allowed: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}."
            )
        if size <= 0:
            raise ValidationError("Uploaded file is empty.")
        if size > settings.max_upload_size_bytes:
            raise ValidationError(
                f"File exceeds the maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )

    async def save(self, user_id: uuid.UUID, file_name: str, data: bytes) -> tuple[str, str]:
        suffix = Path(file_name).suffix.lower()
        user_dir = self.base_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        unique_name = f"{uuid.uuid4().hex}{suffix}"
        absolute_path = user_dir / unique_name
        async with aiofiles.open(absolute_path, "wb") as fh:
            await fh.write(data)

        checksum = hashlib.sha256(data).hexdigest()
        relative_path = str(absolute_path.relative_to(self.base_dir))
        logger.info("Stored upload %s (%d bytes)", relative_path, len(data))
        return relative_path, checksum

    def absolute_path(self, relative_path: str) -> Path:
        return self.base_dir / relative_path

    async def read(self, relative_path: str) -> bytes:
        path = self.absolute_path(relative_path)
        if not path.exists():
            raise ValidationError("Stored file no longer exists.")
        async with aiofiles.open(path, "rb") as fh:
            return await fh.read()

    def delete(self, relative_path: str) -> None:
        path = self.absolute_path(relative_path)
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            logger.warning("Failed to delete %s: %s", relative_path, exc)

storage_service = StorageService()
