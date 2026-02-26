from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.schemas.emotion import EmotionRead  # ייבוא ה-Schema של רגש


class QuestionResponse(BaseModel):
    image_id: int
    image_url: str
    # אנחנו שולחים רשימה של 4 אובייקטים של רגש (הנכון + 3 מסיחים)
    options: List[EmotionRead]

    # הערה: אנחנו לא שולחים כאן את ה-correct_emotion_id 
    # כדי שהילד לא יוכל "לרמות" על ידי בדיקת ה-Network בבוקסר.
    # הבדיקה אם הוא צדק תתבצע בשרת כשהוא ישלח את התשובה.


class LearningSessionRead(BaseModel):
    id: int
    user_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
