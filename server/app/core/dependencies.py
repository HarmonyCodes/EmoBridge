from typing import AsyncGenerator

from app.db import get_session
from app.core.config import settings


async def get_db() -> AsyncGenerator:
    async for session in get_session():
        yield session


def get_settings() -> type(settings):
    return settings
