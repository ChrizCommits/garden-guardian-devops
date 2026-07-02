from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DailyTip(Base):
    __tablename__ = "daily_tips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(140))
    description: Mapped[str] = mapped_column(Text)
    month_or_season: Mapped[str] = mapped_column(String(80))
    action_instruction: Mapped[str] = mapped_column(Text)
    safety_warning: Mapped[str] = mapped_column(Text)
    supported_animals: Mapped[str] = mapped_column(Text)
    points_reward: Mapped[int] = mapped_column(Integer)
    active_from_month: Mapped[int] = mapped_column(Integer)
    active_to_month: Mapped[int] = mapped_column(Integer)
