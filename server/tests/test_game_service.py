import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.services import game_service
from app.schemas import GameTrialCreate
from app.models.image import Image
from app.models.emotion import Emotion
from app.models.user import LearningSession


class FakeResult:
    """מדמה תוצאת execute של SQLAlchemy עבור בדיקות ללא DB."""

    def __init__(self, value=None, values=None):
        self._value = value
        self._values = values or []

    def scalar_one_or_none(self):
        return self._value

    def scalars(self):
        class S:
            def __init__(self, vals):
                self._vals = vals

            def all(self):
                return self._vals

        return S(self._values)


def _mock_db_with_session(owner_id: int) -> AsyncMock:
    """מחזיר DB ממוקק שמחזיר סשן בבעלות owner_id."""
    mock_db = AsyncMock()
    # add הוא סינכרוני ב-SQLAlchemy; AsyncMock היה מחזיר coroutine שלא נצרך
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.execute = AsyncMock(
        return_value=FakeResult(value=LearningSession(id=1, user_id=owner_id))
    )
    return mock_db


def test_start_session_commits_and_refreshes():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = asyncio.run(game_service.start_session(mock_db, user_id=123))

    assert isinstance(result, LearningSession)
    assert result.user_id == 123
    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()


def test_submit_trial_score_and_correctness():
    mock_db = _mock_db_with_session(owner_id=10)

    trial_in = GameTrialCreate(
        session_id=1,
        image_id=2,
        correct_emotion_id=5,
        selected_emotion_id=5,
        response_time_ms=150,
    )

    result = asyncio.run(game_service.submit_trial(mock_db, trial_in, current_user_id=10))
    assert result.is_correct
    assert result.score == 1
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()

    trial_in2 = GameTrialCreate(
        session_id=1,
        image_id=2,
        correct_emotion_id=5,
        selected_emotion_id=7,
    )
    result2 = asyncio.run(game_service.submit_trial(mock_db, trial_in2, current_user_id=10))
    assert not result2.is_correct
    assert result2.score == 0


def test_submit_trial_rejects_foreign_session():
    mock_db = _mock_db_with_session(owner_id=10)

    trial_in = GameTrialCreate(
        session_id=1,
        image_id=2,
        correct_emotion_id=5,
        selected_emotion_id=5,
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(game_service.submit_trial(mock_db, trial_in, current_user_id=99))

    assert exc_info.value.status_code == 403
    mock_db.commit.assert_not_awaited()


def test_end_session_updates_ended_at():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    session = LearningSession(user_id=42)
    session.ended_at = None
    mock_db.get = AsyncMock(return_value=session)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = asyncio.run(game_service.end_session(mock_db, session_id=99, current_user_id=42))
    assert result.ended_at is not None
    assert result.ended_at.tzinfo is not None
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()


def test_end_session_rejects_foreign_session():
    mock_db = AsyncMock()
    mock_db.get = AsyncMock(return_value=LearningSession(user_id=42))
    mock_db.commit = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(game_service.end_session(mock_db, session_id=99, current_user_id=7))

    assert exc_info.value.status_code == 403
    mock_db.commit.assert_not_awaited()


def test_end_session_missing_returns_none():
    mock_db = AsyncMock()
    mock_db.get = AsyncMock(return_value=None)

    result = asyncio.run(game_service.end_session(mock_db, session_id=99, current_user_id=7))
    assert result is None


def test_get_random_question():
    mock_db = AsyncMock()
    image = Image(id=10, url="http://img", emotion_id=3)
    correct = Emotion(id=3, name="happy", emoji=":)", color="#FFD700")
    other1 = Emotion(id=4, name="sad", emoji=":(", color="#4682B4")
    other2 = Emotion(id=5, name="angry", emoji=":!", color="#DC143C")
    other3 = Emotion(id=6, name="surprised", emoji=":o", color="#FF8C00")

    mock_db.execute = AsyncMock(
        side_effect=[
            FakeResult(value=image),
            FakeResult(values=[other1, other2, other3]),
        ]
    )
    mock_db.get = AsyncMock(return_value=correct)

    with patch("random.shuffle", lambda x: x):
        question = asyncio.run(game_service.get_random_question(mock_db))

    assert question.image_id == image.id
    assert question.image_url == image.url
    assert len(question.options) == 4
    # הרגש הנכון חייב להופיע בין האפשרויות
    assert any(o.id == correct.id for o in question.options)
