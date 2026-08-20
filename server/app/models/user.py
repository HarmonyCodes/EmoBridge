from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.time_utils import utc_now
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    # הרשאת ניהול: מאפשרת צפייה בנתוני אנליטיקס של משתמשים אחרים
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    sessions = relationship("LearningSession", back_populates="user", lazy="selectin", cascade="all, delete-orphan")


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    user = relationship("User", back_populates="sessions", lazy="selectin")
    progresses = relationship("GameTrial", back_populates="session", lazy="selectin", cascade="all, delete-orphan")

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
