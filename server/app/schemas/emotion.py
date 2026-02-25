from typing import Optional
from pydantic import BaseModel, ConfigDict


class EmotionCreate(BaseModel):
    name: str
    description: Optional[str] = None


class EmotionRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
