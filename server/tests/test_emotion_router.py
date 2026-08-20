import asyncio
from unittest.mock import AsyncMock, patch

from app.models.emotion import Emotion
from app.models.user import User
from app.routers import emotion_router
from app.schemas import EmotionCreate


def _admin() -> User:
    return User(id=1, username="admin", hashed_password="x", is_admin=True)


def _member() -> User:
    return User(id=2, username="member", hashed_password="x", is_admin=False)


def test_router_create_calls_service():
    emotion_in = EmotionCreate(name="calm", emoji="😌", color="#98FB98")

    fake_emotion = Emotion(name="calm", emoji="😌", color="#98FB98")

    async def run_test():
        with patch("app.services.emotion_service.create_emotion", new=AsyncMock(return_value=fake_emotion)) as mock_fn:
            result = await emotion_router.create_emotion(emotion_in, _admin=_admin(), db=None)
            mock_fn.assert_awaited()
            assert isinstance(result, Emotion)
            assert result.color == "#98FB98"

    asyncio.run(run_test())


def test_router_list_is_available_to_any_member():
    """קריאת רגשות נחוצה למשחק, ולכן פתוחה לכל משתמש מחובר."""
    fake_emotions = [Emotion(name="calm", emoji="😌", color="#98FB98")]

    async def run_test():
        with patch("app.services.emotion_service.list_emotions", new=AsyncMock(return_value=fake_emotions)) as mock_fn:
            result = await emotion_router.list_emotions(current_user=_member(), db=None)
            mock_fn.assert_awaited()
            assert result == fake_emotions

    asyncio.run(run_test())
