from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas, services
from app.core.dependencies import get_current_user
from app.core.time_utils import ensure_utc
from app.db import get_session

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/user-success",
    response_model=schemas.UserAnalyticsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_success_analytics(
    start_date: Annotated[
        datetime | None,
        Query(description="ISO datetime, e.g. 2026-04-01T00:00:00"),
    ] = None,
    end_date: Annotated[
        datetime | None,
        Query(description="ISO datetime, e.g. 2026-04-30T23:59:59"),
    ] = None,
    user_id: Annotated[
        int | None,
        Query(ge=1, description="Optional user filter (admin only)"),
    ] = None,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """
    מחזיר אחוזי הצלחה וזמן תגובה ממוצע לפי טווח תאריכים.
    ולידציית ISO מתבצעת אוטומטית באמצעות טיפוס datetime.
    משתמש רגיל רואה את נתוניו בלבד; אדמין יכול לסנן לפי כל משתמש,
    ובלי user_id מקבל תמונה כוללת של כל המשתמשים.
    """
    normalized_start_date = ensure_utc(start_date)
    normalized_end_date = ensure_utc(end_date)

    if (
        normalized_start_date
        and normalized_end_date
        and normalized_start_date > normalized_end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be earlier than or equal to end_date",
        )

    if current_user.is_admin:
        target_user_id = user_id
    else:
        if user_id is not None and user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view analytics for another user",
            )
        target_user_id = current_user.id

    return await services.analytics_service.get_user_success_analytics(
        db=db,
        start_date=normalized_start_date,
        end_date=normalized_end_date,
        user_id=target_user_id,
    )
