from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GameTrialCreate(BaseModel):
    session_id: int
    image_id: int
    correct_emotion_id: int
    selected_emotion_id: int
    is_correct: bool = False
    response_time_ms: Optional[int] = None


class GameTrialRead(BaseModel):
    id: int
    session_id: int
    image_id: int
    correct_emotion_id: int
    selected_emotion_id: int
    is_correct: bool = False
    score: int = 0
    response_time_ms: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class GameTrialSummaryRead(BaseModel):
    id: int
    session_id: int
    correct_emotion_id: int
    score: int

    model_config = ConfigDict(from_attributes=True)
