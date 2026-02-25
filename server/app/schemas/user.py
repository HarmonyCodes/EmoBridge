from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProgressCreate(BaseModel):
    session_id: int
    emotion_id: int
    score: int = 0


class ProgressRead(BaseModel):
    id: int
    session_id: int
    emotion_id: int
    score: int

    model_config = ConfigDict(from_attributes=True)
