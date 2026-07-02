from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.action import CompletedAction
from app.models.user import User


def _day_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.min, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    return start, end


def has_completion_on_day(session: Session, user_id: int, day: date) -> bool:
    start, end = _day_bounds(day)
    return (
        session.scalar(
            select(CompletedAction)
            .where(CompletedAction.user_id == user_id)
            .where(CompletedAction.completed_at >= start)
            .where(CompletedAction.completed_at < end)
            .limit(1)
        )
        is not None
    )


def update_streak_for_completion(session: Session, user: User, completed_day: date) -> None:
    if has_completion_on_day(session, user.id, completed_day):
        return

    start, _ = _day_bounds(completed_day)
    previous = session.scalar(
        select(CompletedAction)
        .where(CompletedAction.user_id == user.id)
        .where(CompletedAction.completed_at < start)
        .order_by(desc(CompletedAction.completed_at))
        .limit(1)
    )

    if previous is None:
        user.current_streak = 1
    elif previous.completed_at.date() == completed_day - timedelta(days=1):
        user.current_streak += 1
    else:
        user.current_streak = 1

    user.best_streak = max(user.best_streak, user.current_streak)
