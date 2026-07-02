from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AnimalCard(Base):
    __tablename__ = "animal_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    animal_id: Mapped[int] = mapped_column(ForeignKey("animals.id"))
    title: Mapped[str] = mapped_column(String(140))
    fact: Mapped[str] = mapped_column(Text)
    rarity: Mapped[str] = mapped_column(String(40))
    points_value: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String(255))

    animal = relationship("Animal", back_populates="cards")
    earned_by = relationship("UserAnimalCard", back_populates="card")
