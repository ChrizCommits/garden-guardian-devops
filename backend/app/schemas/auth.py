from datetime import datetime

from pydantic import BaseModel, Field


class DemoLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)


class UserResponse(BaseModel):
    id: int
    username: str
    total_points: int
    current_rank: str
    current_streak: int
    best_streak: int
    created_at: datetime
