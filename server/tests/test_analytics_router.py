import asyncio
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.models.user import User
from app.routers import analytics_router
from app.schemas import UserAnalyticsResponse

SERVICE_PATH = "app.services.analytics_service.get_user_success_analytics"

EMPTY_RESPONSE = UserAnalyticsResponse(
    success_rate_percent=0.0,
    average_response_time_ms=0.0,
    emotion_distribution=[],
)


def _user(user_id: int, is_admin: bool = False) -> User:
    return User(
        id=user_id,
        username=f"user{user_id}",
        hashed_password="x",
        is_admin=is_admin,
    )


def _call(current_user: User, **kwargs):
    """מריץ את ה-endpoint עם השירות ממוקק, ומחזיר (תוצאה, mock)."""

    async def run():
        with patch(SERVICE_PATH, new=AsyncMock(return_value=EMPTY_RESPONSE)) as mock_fn:
            result = await analytics_router.get_user_success_analytics(
                current_user=current_user,
                db=None,
                **kwargs,
            )
            return result, mock_fn

    return asyncio.run(run())


def test_regular_user_is_scoped_to_own_data():
    """בלי user_id, משתמש רגיל מקבל את נתוניו בלבד ולא תמונה גלובלית."""
    result, mock_fn = _call(_user(5))

    assert result is EMPTY_RESPONSE
    mock_fn.assert_awaited_once()
    assert mock_fn.await_args.kwargs["user_id"] == 5


def test_regular_user_may_request_own_id():
    _, mock_fn = _call(_user(5), user_id=5)

    assert mock_fn.await_args.kwargs["user_id"] == 5


def test_regular_user_cannot_request_another_user():
    with pytest.raises(HTTPException) as exc_info:
        _call(_user(5), user_id=9)

    assert exc_info.value.status_code == 403


def test_admin_may_request_another_user():
    _, mock_fn = _call(_user(1, is_admin=True), user_id=9)

    assert mock_fn.await_args.kwargs["user_id"] == 9


def test_admin_without_user_id_gets_global_view():
    """אדמין בלי user_id מקבל תמונה חוצת-משתמשים, כלומר סינון None."""
    _, mock_fn = _call(_user(1, is_admin=True))

    assert mock_fn.await_args.kwargs["user_id"] is None


def test_inverted_date_range_is_rejected():
    start = datetime(2026, 4, 30, tzinfo=timezone.utc)
    end = datetime(2026, 4, 1, tzinfo=timezone.utc)

    with pytest.raises(HTTPException) as exc_info:
        _call(_user(5), start_date=start, end_date=end)

    assert exc_info.value.status_code == 400


def test_mixed_naive_and_aware_dates_are_normalized():
    """
    רגרסיה: השוואה בין datetime נאיבי למודע זרקה TypeError.
    הראוטר מנרמל את שניהם ל-UTC לפני ההשוואה ולפני המעבר לשירות.
    """
    naive_start = datetime(2026, 4, 1, 0, 0, 0)
    aware_end = datetime(2026, 4, 30, 0, 0, 0, tzinfo=timezone(timedelta(hours=3)))

    _, mock_fn = _call(_user(5), start_date=naive_start, end_date=aware_end)

    passed_start = mock_fn.await_args.kwargs["start_date"]
    passed_end = mock_fn.await_args.kwargs["end_date"]

    assert passed_start.tzinfo is not None
    assert passed_start == naive_start.replace(tzinfo=timezone.utc)
    assert passed_end.utcoffset() == timedelta(0)
    assert passed_end == aware_end
