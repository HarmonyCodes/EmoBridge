from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app  import models, schemas, services
from app.core.dependencies import get_current_admin_user, get_current_user
from app.db import get_session

router = APIRouter(prefix="/emotions", tags=["emotions"])


# ניהול תוכן הרגשות מוגבל לאדמין; קריאה פתוחה לכל משתמש מחובר לצורך המשחק
@router.post("/", response_model=schemas.EmotionRead, status_code=status.HTTP_201_CREATED)
async def create_emotion(
    emotion_in: schemas.EmotionCreate,
    _admin: models.User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_session),
):
    return await services.emotion_service.create_emotion(db, emotion_in)


@router.get("/", response_model=List[schemas.EmotionRead])
async def list_emotions(
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await services.emotion_service.list_emotions(db, limit=limit)


@router.get("/{emotion_id}", response_model=schemas.EmotionRead)
async def read_emotion(
    emotion_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    emotion = await services.emotion_service.get_emotion(db, emotion_id)
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion

@router.get("/{emotion_id}/with-images", response_model=schemas.EmotionRead) 
async def read_emotion_with_images(
    emotion_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    emotion = await services.emotion_service.get_emotion_with_images(db, emotion_id)
    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion


@router.delete("/{emotion_id}")
async def delete_emotion(
    emotion_id: int,
    _admin: models.User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_session),
):
    ok = await services.emotion_service.delete_emotion(db, emotion_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return {"ok": True}
