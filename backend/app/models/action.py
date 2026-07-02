from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CompletedAction(Base):
    __tablename__ = "completed_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    daily_tip_id: Mapped[int] = mapped_column(ForeignKey("daily_tips.id"))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    points_awarded: Mapped[int] = mapped_column(Integer)

    user = relationship("User", back_populates="completed_actions")
    tip = relationship("DailyTip")


class UserAnimalCard(Base):
    __tablename__ = "user_animal_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("animal_cards.id"))
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    source_tip_id: Mapped[int] = mapped_column(ForeignKey("daily_tips.id"))

    user = relationship("User", back_populates="earned_cards")
    card = relationship("AnimalCard", back_populates="earned_by")
    source_tip = relationship("DailyTip")
