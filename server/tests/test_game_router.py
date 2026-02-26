import asyncio
from unittest.mock import AsyncMock, patch

from app.routers import game_router
from app.models.user import LearningSession
from app.models.image import Image
from app.models.emotion import Emotion
from app.schemas import GameTrialCreate


def test_router_start_session_calls_service():
    fake_session = LearningSession(user_id=7)

    async def run():
        with patch("app.services.game_service.start_session", new=AsyncMock(return_value=fake_session)) as mock_fn:
            result = await game_router.start_session(user_id=7, db=None)
            mock_fn.assert_awaited()
            assert result is fake_session

    asyncio.run(run())


def test_router_get_random_question_calls_service():
    fake_question = {
        "image_id": 1,
        "image_url": "http://x",
        "options": [],
    }

    async def run():
        with patch("app.services.game_service.get_random_question", new=AsyncMock(return_value=fake_question)) as mock_fn:
            result = await game_router.get_random_question(db=None)
            mock_fn.assert_awaited()
            assert result == fake_question

    asyncio.run(run())


def test_router_submit_trial_calls_service():
    trial_in = GameTrialCreate(session_id=1, image_id=2, correct_emotion_id=3, selected_emotion_id=3)
    fake_trial = object()

    async def run():
        with patch("app.services.game_service.submit_trial", new=AsyncMock(return_value=fake_trial)) as mock_fn:
            result = await game_router.submit_trial(trial_in, db=None)
            mock_fn.assert_awaited()
            assert result is fake_trial

    asyncio.run(run())


def test_router_end_session_calls_service():
    fake_session = LearningSession(user_id=5)

    async def run():
        with patch("app.services.game_service.end_session", new=AsyncMock(return_value=fake_session)) as mock_fn:
            result = await game_router.end_session(session_id=13, db=None)
            mock_fn.assert_awaited()
            assert result is fake_session

    asyncio.run(run())
