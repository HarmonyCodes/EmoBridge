from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)

    sessions = relationship("LearningSession", back_populates="user", lazy="selectin")


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user = relationship("User", back_populates="sessions", lazy="selectin")
    progresses = relationship("GameTrial", back_populates="session", lazy="selectin")


class GameTrial(Base):
    __tablename__ = "game_trials"

class GameTrial(Base):
    __tablename__ = "game_trials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"), nullable=False)
    image_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=False) # איזו תמונה הוצגה
    correct_emotion_id: Mapped[int] = mapped_column(ForeignKey("emotions.id"), nullable=False)
    selected_emotion_id: Mapped[int] = mapped_column(ForeignKey("emotions.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0)

    is_correct: Mapped[bool] = mapped_column(default=False)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True) # זמן תגובה במילישניות
    session = relationship("LearningSession", back_populates="progresses", lazy="selectin")
