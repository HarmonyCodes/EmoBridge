from datetime import datetime, timedelta

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_user_success_analytics(
    db: AsyncSession,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    user_id: int | None = None,
) -> schemas.UserAnalyticsResponse:
    """
    מחשב מדדי הצלחה וזמן תגובה בטווח תאריכים מוגדר.
    ברירת מחדל: 30 הימים האחרונים.
    """
    resolved_end_date = end_date or datetime.utcnow()
    resolved_start_date = start_date or (resolved_end_date - timedelta(days=30))

    filters = [
        models.LearningSession.started_at >= resolved_start_date,
        models.LearningSession.started_at <= resolved_end_date,
    ]
    if user_id is not None:
        filters.append(models.LearningSession.user_id == user_id)

    overall_stmt = (
        select(
            func.count(models.GameTrial.id).label("total_trials"),
            (
                func.coalesce(
                    func.avg(
                        case(
                            (models.GameTrial.is_correct.is_(True), 1.0),
                            else_=0.0,
                        )
                    ),
                    0.0,
                )
                * 100.0
            ).label("success_rate_percent"),
            func.coalesce(func.avg(models.GameTrial.response_time_ms), 0.0).label(
                "average_response_time_ms"
            ),
        )
        .select_from(models.GameTrial)
        .join(
            models.LearningSession,
            models.GameTrial.session_id == models.LearningSession.id,
        )
        .where(*filters)
    )
    overall_result = await db.execute(overall_stmt)
    total_trials, success_rate_percent, average_response_time_ms = overall_result.one()

    distribution_stmt = (
        select(
            models.Emotion.id.label("emotion_id"),
            models.Emotion.name.label("emotion_name"),
            func.count(models.GameTrial.id).label("attempts"),
            func.sum(
                case(
                    (models.GameTrial.is_correct.is_(True), 1),
                    else_=0,
                )
            ).label("correct_attempts"),
        )
        .select_from(models.GameTrial)
        .join(
            models.LearningSession,
            models.GameTrial.session_id == models.LearningSession.id,
        )
        .join(
            models.Emotion,
            models.GameTrial.correct_emotion_id == models.Emotion.id,
        )
        .where(*filters)
        .group_by(models.Emotion.id, models.Emotion.name)
        .order_by(models.Emotion.name.asc())
    )
    distribution_result = await db.execute(distribution_stmt)
    distribution_rows = distribution_result.all()

    emotion_distribution: list[schemas.EmotionSuccessDistribution] = []
    for row in distribution_rows:
        attempts = int(row.attempts or 0)
        correct_attempts = int(row.correct_attempts or 0)
        per_emotion_success = (correct_attempts / attempts * 100.0) if attempts > 0 else 0.0

        emotion_distribution.append(
            schemas.EmotionSuccessDistribution(
                emotion_id=int(row.emotion_id),
                emotion_name=row.emotion_name,
                attempts=attempts,
                correct_attempts=correct_attempts,
                success_rate_percent=round(per_emotion_success, 2),
            )
        )

    # במקרה שאין נתונים בכלל בטווח, מחזירים מבנה תקין עם אפסים.
    if int(total_trials or 0) == 0:
        return schemas.UserAnalyticsResponse(
            success_rate_percent=0.0,
            average_response_time_ms=0.0,
            emotion_distribution=[],
        )

    return schemas.UserAnalyticsResponse(
        success_rate_percent=round(float(success_rate_percent or 0.0), 2),
        average_response_time_ms=round(float(average_response_time_ms or 0.0), 2),
        emotion_distribution=emotion_distribution,
    )
