from datetime import datetime
from typing import List, Optional
import random

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def start_session(db: AsyncSession, user_id: int) -> models.LearningSession:
    session = models.LearningSession(user_id=user_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_random_question(db: AsyncSession) -> schemas.QuestionResponse:
    # pick a random image
    # note: ordering by random() is generic; DB-specific behavior assumed
    result = await db.execute(select(models.Image).order_by(func.random()).limit(1))
    image = result.scalar_one_or_none()
    if not image:
        raise ValueError("No images available")

    # load correct emotion
    correct = await db.get(models.Emotion, image.emotion_id)
    if not correct:
        raise ValueError("Image has no associated emotion")

    # pick 3 distractor emotions
    distractor_stmt = (
        select(models.Emotion)
        .where(models.Emotion.id != correct.id)
        .order_by(func.random())
        .limit(3)
    )
    resp = await db.execute(distractor_stmt)
    others = resp.scalars().all()

    options: List[models.Emotion] = [correct] + others
    # shuffle to randomize order
    random.shuffle(options)

    return schemas.QuestionResponse(
        image_id=image.id,
        image_url=image.url,
        options=options,
    )


async def submit_trial(
    db: AsyncSession, trial_in: schemas.GameTrialCreate
) -> models.GameTrial:
    is_correct = trial_in.selected_emotion_id == trial_in.correct_emotion_id
    score = 1 if is_correct else 0
    trial = models.GameTrial(
        session_id=trial_in.session_id,
        image_id=trial_in.image_id,
        correct_emotion_id=trial_in.correct_emotion_id,
        selected_emotion_id=trial_in.selected_emotion_id,
        is_correct=is_correct,
        score=score,
        response_time_ms=trial_in.response_time_ms,
    )
    db.add(trial)
    await db.commit()
    await db.refresh(trial)
    return trial


async def end_session(db: AsyncSession, session_id: int) -> Optional[models.LearningSession]:
    session = await db.get(models.LearningSession, session_id)
    if not session:
        return None
    session.ended_at = datetime.utcnow()
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session
