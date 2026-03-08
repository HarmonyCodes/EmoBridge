from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.services import auth_service


async def create_user(db: AsyncSession, user_in: schemas.UserCreate) -> models.User:
    hashed = auth_service.get_password_hash(user_in.password)
    user = models.User(username=user_in.username, email=user_in.email, hashed_password=hashed)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()


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
