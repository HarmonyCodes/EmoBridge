import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.routers import game_router
from app.models.user import LearningSession, User
from app.schemas import GameTrialCreate


def _user(user_id: int) -> User:
    return User(id=user_id, username=f"user{user_id}", hashed_password="x")


def test_router_start_session_calls_service():
    fake_session = LearningSession(user_id=7)

    async def run():
        with patch("app.services.game_service.start_session", new=AsyncMock(return_value=fake_session)) as mock_fn:
            result = await game_router.start_session(current_user=_user(7), db=None)
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
            result = await game_router.get_random_question(current_user=_user(7), db=None)
            mock_fn.assert_awaited()
            assert result == fake_question

    asyncio.run(run())


def test_router_get_random_question_maps_missing_images_to_404():
    async def run():
        with patch(
            "app.services.game_service.get_random_question",
            new=AsyncMock(side_effect=ValueError("No images available")),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await game_router.get_random_question(current_user=_user(7), db=None)
            assert exc_info.value.status_code == 404

    asyncio.run(run())


def test_router_submit_trial_passes_current_user():
    trial_in = GameTrialCreate(session_id=1, image_id=2, correct_emotion_id=3, selected_emotion_id=3)
    fake_trial = object()

    async def run():
        with patch("app.services.game_service.submit_trial", new=AsyncMock(return_value=fake_trial)) as mock_fn:
            result = await game_router.submit_trial(trial_in, current_user=_user(42), db=None)
            mock_fn.assert_awaited_once_with(None, trial_in, 42)
            assert result is fake_trial

    asyncio.run(run())


def test_router_end_session_passes_current_user():
    fake_session = LearningSession(user_id=5)

    async def run():
        with patch("app.services.game_service.end_session", new=AsyncMock(return_value=fake_session)) as mock_fn:
            result = await game_router.end_session(session_id=13, current_user=_user(5), db=None)
            mock_fn.assert_awaited_once_with(None, 13, 5)
            assert result is fake_session

    asyncio.run(run())


def test_router_end_session_missing_returns_404():
    async def run():
        with patch("app.services.game_service.end_session", new=AsyncMock(return_value=None)):
            with pytest.raises(HTTPException) as exc_info:
                await game_router.end_session(session_id=13, current_user=_user(5), db=None)
            assert exc_info.value.status_code == 404

    asyncio.run(run())
