import asyncio
from unittest.mock import AsyncMock, MagicMock

from app.services import emotion_service
from app.schemas import EmotionCreate
from app.models.emotion import Emotion


def test_create_emotion_persists_all_fields():
    """color הוא nullable=False, ולכן חייב לעבור מהסכמה למודל."""
    mock_db = AsyncMock()
    # add הוא סינכרוני ב-SQLAlchemy; AsyncMock היה מחזיר coroutine שלא נצרך
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    emotion_in = EmotionCreate(name="joy", emoji="😊", color="#FFD700")

    result = asyncio.run(emotion_service.create_emotion(mock_db, emotion_in))

    assert isinstance(result, Emotion)
    assert result.name == "joy"
    assert result.emoji == "😊"
    assert result.color == "#FFD700"
    mock_db.add.assert_called_once_with(result)
    mock_db.commit.assert_awaited()
    mock_db.refresh.assert_awaited()
