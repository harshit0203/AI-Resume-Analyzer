from __future__ import annotations

import asyncio

from app.core.database import Base, engine
import app.models

async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("All tables created.")

if __name__ == "__main__":
    asyncio.run(main())
