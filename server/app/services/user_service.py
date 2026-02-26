from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_user(db: AsyncSession, user_in: schemas.UserCreate) -> models.User:
    (hashed_password)
    user = models.User(username=user_in.username, email=user_in.email, hashed_password=user_in.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession, limit: int = 100) -> List[models.User]:
    result = await db.execute(select(models.User).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_in: schemas.UserCreate) -> Optional[models.User]:
    user = await get_user(db, user_id)
    if not user:
        return None
    user.username = user_in.username
    user.email = user_in.email
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
