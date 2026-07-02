from datetime import datetime

from pydantic import BaseModel

from app.schemas.garden import EarnedAnimalCardResponse


class RecentActionResponse(BaseModel):
    id: int
    tip_id: int
    tip_title: str
    completed_at: datetime
    points_awarded: int


class FavoriteAnimalResponse(BaseModel):
    animal_name: str
    help_count: int


class ProfileResponse(BaseModel):
    id: int
    username: str
    total_points: int
    current_rank: str
    current_streak: int
    best_streak: int
    collected_cards: list[EarnedAnimalCardResponse]
    recent_actions: list[RecentActionResponse]
    favorite_animals: list[FavoriteAnimalResponse]


class CardsResponse(BaseModel):
    cards: list[EarnedAnimalCardResponse]
