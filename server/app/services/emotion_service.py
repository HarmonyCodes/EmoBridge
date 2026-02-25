from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_emotion(db: AsyncSession, emotion_in: schemas.EmotionCreate) -> models.Emotion:
    emotion = models.Emotion(name=emotion_in.name, description=emotion_in.description)
    db.add(emotion)
    await db.commit()
    await db.refresh(emotion)
    return emotion


async def get_emotion(db: AsyncSession, emotion_id: int) -> Optional[models.Emotion]:
    result = await db.execute(select(models.Emotion).where(models.Emotion.id == emotion_id))
    return result.scalar_one_or_none()


async def list_emotions(db: AsyncSession, limit: int = 100) -> List[models.Emotion]:
    result = await db.execute(select(models.Emotion).limit(limit))
    return result.scalars().all()


async def delete_emotion(db: AsyncSession, emotion_id: int) -> bool:
    emotion = await get_emotion(db, emotion_id)
    if not emotion:
        return False
    await db.delete(emotion)
    await db.commit()
    return True
