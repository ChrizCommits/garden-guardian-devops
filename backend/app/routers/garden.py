from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_session
from app.models.animal import Animal
from app.models.card import AnimalCard
from app.models.tip import DailyTip
from app.models.user import User
from app.schemas.garden import (
    AnimalCardResponse,
    AnimalResponse,
    CompleteRequest,
    CompleteResponse,
    IntendRequest,
    IntendResponse,
    TodayTipResponse,
)
from app.services.ranks import get_rank
from app.services.rewards import complete_tip
from app.services.seasonal_tips import decode_supported_animals, get_tip_for_date

router = APIRouter(prefix="/api", tags=["garden"])


def serialize_animal(animal: Animal) -> AnimalResponse:
    return AnimalResponse(
        id=animal.id,
        name=animal.name,
        category=animal.category,
        description=animal.description,
        image_url=animal.image_url,
        safe_support_notes=animal.safe_support_notes,
        unsafe_foods=animal.unsafe_foods,
    )


def serialize_card(card: AnimalCard) -> AnimalCardResponse:
    return AnimalCardResponse(
        id=card.id,
        animal_id=card.animal_id,
        animal_name=card.animal.name,
        title=card.title,
        fact=card.fact,
        rarity=card.rarity,
        points_value=card.points_value,
        image_url=card.image_url,
    )


def get_user_or_404(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Demo user not found")
    return user


def get_tip_or_404(session: Session, tip_id: int) -> DailyTip:
    tip = session.get(DailyTip, tip_id)
    if tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return tip


@router.get("/today", response_model=TodayTipResponse)
def get_today(session: Session = Depends(get_session)) -> TodayTipResponse:
    tip = get_tip_for_date(session)
    supported_names = decode_supported_animals(tip)
    animals = session.scalars(select(Animal).where(Animal.name.in_(supported_names))).all()
    cards = (
        session.scalars(
            select(AnimalCard)
            .options(joinedload(AnimalCard.animal))
            .join(AnimalCard.animal)
            .where(Animal.name.in_(supported_names))
        )
        .unique()
        .all()
    )
    return TodayTipResponse(
        id=tip.id,
        title=tip.title,
        description=tip.description,
        month_or_season=tip.month_or_season,
        action_instruction=tip.action_instruction,
        safety_warning=tip.safety_warning,
        supported_animals=[serialize_animal(animal) for animal in animals],
        points_reward=tip.points_reward,
        possible_reward_cards=[serialize_card(card) for card in cards],
    )


@router.get("/animals", response_model=list[AnimalResponse])
def get_animals(session: Session = Depends(get_session)) -> list[AnimalResponse]:
    animals = session.scalars(select(Animal).order_by(Animal.name)).all()
    return [serialize_animal(animal) for animal in animals]


@router.post("/tips/{tip_id}/intend", response_model=IntendResponse)
def intend_tip(
    tip_id: int,
    payload: IntendRequest,
    session: Session = Depends(get_session),
) -> IntendResponse:
    get_tip_or_404(session, tip_id)
    get_user_or_404(session, payload.user_id)
    return IntendResponse(message="Lovely. Come back and mark it done after you complete the action.", awarded=False)


@router.post("/tips/{tip_id}/complete", response_model=CompleteResponse)
def complete_tip_endpoint(
    tip_id: int,
    payload: CompleteRequest,
    session: Session = Depends(get_session),
) -> CompleteResponse:
    tip = get_tip_or_404(session, tip_id)
    user = get_user_or_404(session, payload.user_id)
    result = complete_tip(session, user, tip)
    card = result["unlocked_card"]
    message = "Action saved. You unlocked a matching animal card." if result["awarded"] else "Already completed today. No extra points awarded."
    return CompleteResponse(
        awarded=bool(result["awarded"]),
        message=message,
        points_awarded=int(result["points_awarded"]),
        total_points=user.total_points,
        current_rank=get_rank(user.total_points),
        current_streak=user.current_streak,
        best_streak=user.best_streak,
        unlocked_card=serialize_card(card) if card else None,
    )
