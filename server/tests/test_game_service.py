import asyncio
from unittest.mock import AsyncMock, patch

from app.services import game_service
from app.schemas import GameTrialCreate
from app.models.image import Image
from app.models.emotion import Emotion
from app.models.user import LearningSession


def test_start_session_commits_and_refreshes():
    mock_db = AsyncMock()
    added = []

    def add(obj):
        added.append(obj)

    mock_db.add.side_effect = add
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = asyncio.run(game_service.start_session(mock_db, user_id=123))

    assert isinstance(result, LearningSession)
    assert result.user_id == 123
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()


def test_submit_trial_score_and_correctness():
    mock_db = AsyncMock()
    mock_db.add.side_effect = lambda o: None
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    trial_in = GameTrialCreate(
        session_id=1,
        image_id=2,
        correct_emotion_id=5,
        selected_emotion_id=5,
        response_time_ms=150,
    )

    result = asyncio.run(game_service.submit_trial(mock_db, trial_in))
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
    result2 = asyncio.run(game_service.submit_trial(mock_db, trial_in2))
    assert not result2.is_correct
    assert result2.score == 0


def test_end_session_updates_ended_at():
    mock_db = AsyncMock()
    session = LearningSession(user_id=42)
    session.ended_at = None
    mock_db.get = AsyncMock(return_value=session)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    result = asyncio.run(game_service.end_session(mock_db, session_id=99))
    assert result.ended_at is not None
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()


def test_get_random_question():
    mock_db = AsyncMock()
    image = Image(id=10, url="http://img", emotion_id=3)
    correct = Emotion(id=3, name="happy", emoji=":)")
    other1 = Emotion(id=4, name="sad", emoji=":(")
    other2 = Emotion(id=5, name="angry", emoji=":!")
    other3 = Emotion(id=6, name="surprised", emoji=":o")

    class FakeResult:
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

    mock_db.execute = AsyncMock(
        side_effect=[
            FakeResult(value=image),
            FakeResult(values=[other1, other2, other3]),
        ]
    )

    with patch("random.shuffle", lambda x: x):
        question = asyncio.run(game_service.get_random_question(mock_db))

    assert question.image_id == image.id
    assert question.image_url == image.url
    assert len(question.options) == 4
    # correct emotion should be present
    assert any(o.id == correct.id for o in question.options)
