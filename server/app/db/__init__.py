import os
from typing import AsyncGenerator
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
   settings.DATABASE_URL
,
)


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
