from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.action import CompletedAction, UserAnimalCard
from app.models.card import AnimalCard
from app.models.tip import DailyTip
from app.models.user import User
from app.services.seasonal_tips import decode_supported_animals
from app.services.streaks import update_streak_for_completion


def _day_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.min, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    return start, end


def already_completed_tip_today(
    session: Session,
    user_id: int,
    tip_id: int,
    completed_day: date,
) -> CompletedAction | None:
    start, end = _day_bounds(completed_day)
    return session.scalar(
        select(CompletedAction)
        .where(CompletedAction.user_id == user_id)
        .where(CompletedAction.daily_tip_id == tip_id)
        .where(CompletedAction.completed_at >= start)
        .where(CompletedAction.completed_at < end)
        .limit(1)
    )


def choose_matching_card(session: Session, tip: DailyTip, user_id: int) -> AnimalCard:
    supported = set(decode_supported_animals(tip))
    matching_cards = (
        session.scalars(
            select(AnimalCard)
            .options(joinedload(AnimalCard.animal))
            .join(AnimalCard.animal)
        )
        .unique()
        .all()
    )
    matching_cards = [card for card in matching_cards if card.animal.name in supported]
    matching_cards.sort(key=lambda card: (card.points_value, card.id))

    earned_card_ids = set(
        session.scalars(select(UserAnimalCard.card_id).where(UserAnimalCard.user_id == user_id)).all()
    )
    for card in matching_cards:
        if card.id not in earned_card_ids:
            return card
    return matching_cards[0]


def complete_tip(session: Session, user: User, tip: DailyTip, completed_day: date | None = None) -> dict[str, object]:
    completed_day = completed_day or date.today()
    duplicate = already_completed_tip_today(session, user.id, tip.id, completed_day)
    if duplicate is not None:
        return {"awarded": False, "unlocked_card": None, "points_awarded": 0}

    update_streak_for_completion(session, user, completed_day)
    user.total_points += tip.points_reward
    completed_at = datetime.combine(completed_day, time(hour=12), tzinfo=timezone.utc)
    action = CompletedAction(
        user_id=user.id,
        daily_tip_id=tip.id,
        completed_at=completed_at,
        points_awarded=tip.points_reward,
    )
    session.add(action)
    session.flush()

    card = choose_matching_card(session, tip, user.id)
    earned = UserAnimalCard(
        user_id=user.id,
        card_id=card.id,
        earned_at=completed_at,
        source_tip_id=tip.id,
    )
    session.add(earned)
    session.commit()
    session.refresh(user)
    session.refresh(card)
    return {"awarded": True, "unlocked_card": card, "points_awarded": tip.points_reward}
