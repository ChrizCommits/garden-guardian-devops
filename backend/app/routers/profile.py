from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_session
from app.models.action import CompletedAction, UserAnimalCard
from app.models.card import AnimalCard
from app.models.user import User
from app.routers.garden import serialize_card
from app.schemas.garden import EarnedAnimalCardResponse
from app.schemas.profile import CardsResponse, FavoriteAnimalResponse, ProfileResponse, RecentActionResponse
from app.services.ranks import get_rank
from app.services.seasonal_tips import decode_supported_animals

router = APIRouter(prefix="/api", tags=["profile"])


def get_user_or_404(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Demo user not found")
    return user


def serialize_earned_card(earned: UserAnimalCard) -> EarnedAnimalCardResponse:
    card = serialize_card(earned.card)
    return EarnedAnimalCardResponse(
        **card.model_dump(),
        earned_at=earned.earned_at,
        source_tip_id=earned.source_tip_id,
    )


def get_earned_cards(session: Session, user_id: int) -> list[UserAnimalCard]:
    return (
        session.scalars(
            select(UserAnimalCard)
            .options(joinedload(UserAnimalCard.card).joinedload(AnimalCard.animal))
            .where(UserAnimalCard.user_id == user_id)
            .order_by(desc(UserAnimalCard.earned_at))
        )
        .unique()
        .all()
    )


def favorite_animals(actions: list[CompletedAction]) -> list[FavoriteAnimalResponse]:
    counts: Counter[str] = Counter()
    for action in actions:
        for animal_name in decode_supported_animals(action.tip):
            counts[animal_name] += 1
    return [
        FavoriteAnimalResponse(animal_name=name, help_count=count)
        for name, count in counts.most_common()
    ]


@router.get("/profile", response_model=ProfileResponse)
def get_profile(user_id: int = Query(), session: Session = Depends(get_session)) -> ProfileResponse:
    user = get_user_or_404(session, user_id)
    earned_cards = get_earned_cards(session, user.id)
    actions = (
        session.scalars(
            select(CompletedAction)
            .options(joinedload(CompletedAction.tip))
            .where(CompletedAction.user_id == user.id)
            .order_by(desc(CompletedAction.completed_at))
        )
        .unique()
        .all()
    )
    return ProfileResponse(
        id=user.id,
        username=user.username,
        total_points=user.total_points,
        current_rank=get_rank(user.total_points),
        current_streak=user.current_streak,
        best_streak=user.best_streak,
        collected_cards=[serialize_earned_card(card) for card in earned_cards],
        recent_actions=[
            RecentActionResponse(
                id=action.id,
                tip_id=action.daily_tip_id,
                tip_title=action.tip.title,
                completed_at=action.completed_at,
                points_awarded=action.points_awarded,
            )
            for action in actions[:10]
        ],
        favorite_animals=favorite_animals(actions),
    )


@router.get("/cards", response_model=CardsResponse)
def get_cards(user_id: int = Query(), session: Session = Depends(get_session)) -> CardsResponse:
    get_user_or_404(session, user_id)
    return CardsResponse(cards=[serialize_earned_card(card) for card in get_earned_cards(session, user_id)])
