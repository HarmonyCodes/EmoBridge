import asyncio
from unittest.mock import AsyncMock, patch

from app.routers import emotion_router
from app.schemas import EmotionCreate
from app.models.emotion import Emotion


def test_router_create_calls_service():
    emotion_in = EmotionCreate(name="calm", description="relaxed")

    fake_emotion = Emotion(name="calm", description="relaxed")

    async def run_test():
        with patch("app.services.emotion_service.create_emotion", new=AsyncMock(return_value=fake_emotion)) as mock_fn:
            result = await emotion_router.create_emotion(emotion_in, db=None)
            mock_fn.assert_awaited()
            assert isinstance(result, Emotion)

    asyncio.run(run_test())
