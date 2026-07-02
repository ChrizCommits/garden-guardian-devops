from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(255))
    safe_support_notes: Mapped[str] = mapped_column(Text)
    unsafe_foods: Mapped[str] = mapped_column(Text)

    cards = relationship("AnimalCard", back_populates="animal")
