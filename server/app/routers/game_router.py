from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, models
from app.db import get_session
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/start_session", response_model=schemas.LearningSessionRead, status_code=status.HTTP_201_CREATED)
async def start_session(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    session = await services.game_service.start_session(db, current_user.id)
    return session


@router.get("/random_question", response_model=schemas.QuestionResponse)
async def get_random_question(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        return await services.game_service.get_random_question(db)
    except ValueError as exc:
        # turn into 404 if no images
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/submit_trial", response_model=schemas.GameTrialRead)
async def submit_trial(trial_in: schemas.GameTrialCreate, current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await services.game_service.submit_trial(db, trial_in, current_user.id)


@router.post("/end_session", response_model=schemas.LearningSessionRead)
async def end_session(session_id: int, db: AsyncSession = Depends(get_session)):
    session = await services.game_service.end_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
