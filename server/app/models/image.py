from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    emotion_id: Mapped[int] = mapped_column(Integer, ForeignKey("emotions.id"), nullable=True)

    emotion: Mapped["Emotion"] = relationship("Emotion", back_populates="images")
