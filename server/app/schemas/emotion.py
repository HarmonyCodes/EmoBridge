from typing import Optional
from pydantic import BaseModel, ConfigDict


class EmotionCreate(BaseModel):
    name: str
    emoji: str
    color: str

class EmotionRead(BaseModel):
    id: int
    name: str
    emoji: str
    color: str
    
    model_config = ConfigDict(from_attributes=True)
