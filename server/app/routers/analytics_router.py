from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services
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
        Query(ge=1, description="Optional user filter"),
    ] = None,
    db: AsyncSession = Depends(get_session),
):
    """
    מחזיר אחוזי הצלחה וזמן תגובה ממוצע לפי טווח תאריכים.
    ולידציית ISO מתבצעת אוטומטית באמצעות טיפוס datetime.
    """
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be earlier than or equal to end_date",
        )

    return await services.analytics_service.get_user_success_analytics(
        db=db,
        start_date=start_date,
        end_date=end_date,
        user_id=user_id,
    )
