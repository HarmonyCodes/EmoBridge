from pydantic import BaseModel


class EmotionSuccessDistribution(BaseModel):
    emotion_id: int
    emotion_name: str
    attempts: int
    correct_attempts: int
    success_rate_percent: float


class UserAnalyticsResponse(BaseModel):
    success_rate_percent: float
    average_response_time_ms: float
    emotion_distribution: list[EmotionSuccessDistribution]
