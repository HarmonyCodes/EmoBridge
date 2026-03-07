import os
import urllib.parse
from app.core.config import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = settings.DATABASE_URL
print(f"DEBUG: Connecting to {DATABASE_URL}") # שורה זמנית לבדיקה
print("FINAL URL:", DATABASE_URL)# שורה זמנית לבדיקה

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
