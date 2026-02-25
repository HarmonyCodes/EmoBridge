from typing import Optional
from pydantic import BaseModel, ConfigDict


class ImageCreate(BaseModel):
    url: str
    emotion_id: Optional[int] = None


class ImageRead(BaseModel):
    id: int
    url: str
    emotion_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
