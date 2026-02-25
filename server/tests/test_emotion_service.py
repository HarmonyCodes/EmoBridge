import asyncio
from unittest.mock import AsyncMock

from app.services import emotion_service
from app.schemas import EmotionCreate
from app.models.emotion import Emotion


def test_create_emotion_commits_and_refreshes():
    mock_db = AsyncMock()

    added = []

    def add(obj):
        # emulate SQLAlchemy add
        added.append(obj)

    mock_db.add.side_effect = add
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    emotion_in = EmotionCreate(name="joy", description="positive")

    result = asyncio.run(emotion_service.create_emotion(mock_db, emotion_in))

    assert isinstance(result, Emotion)
    assert result.name == "joy"
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()
