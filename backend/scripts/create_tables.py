"""Bootstrap helper: create all tables directly from SQLAlchemy metadata.

Useful for local development / first run. For production use Alembic migrations
(`alembic upgrade head`) which are the source of truth for schema changes.

Run with:  python -m scripts.create_tables
"""
from __future__ import annotations

import asyncio

from app.core.database import Base, engine
import app.models  # noqa: F401  (register all models on Base.metadata)


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("All tables created.")


if __name__ == "__main__":
    asyncio.run(main())
