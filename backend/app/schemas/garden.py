from datetime import datetime

from pydantic import BaseModel


class AnimalResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    image_url: str
    safe_support_notes: str
    unsafe_foods: str


class AnimalCardResponse(BaseModel):
    id: int
    animal_id: int
    animal_name: str
    title: str
    fact: str
    rarity: str
    points_value: int
    image_url: str


class EarnedAnimalCardResponse(AnimalCardResponse):
    earned_at: datetime
    source_tip_id: int


class TodayTipResponse(BaseModel):
    id: int
    title: str
    description: str
    month_or_season: str
    action_instruction: str
    safety_warning: str
    supported_animals: list[AnimalResponse]
    points_reward: int
    possible_reward_cards: list[AnimalCardResponse]


class IntendRequest(BaseModel):
    user_id: int


class IntendResponse(BaseModel):
    message: str
    awarded: bool


class CompleteRequest(BaseModel):
    user_id: int


class CompleteResponse(BaseModel):
    awarded: bool
    message: str
    points_awarded: int
    total_points: int
    current_rank: str
    current_streak: int
    best_streak: int
    unlocked_card: AnimalCardResponse | None
