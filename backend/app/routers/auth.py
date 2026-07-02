from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.user import User
from app.schemas.auth import DemoLoginRequest, UserResponse
from app.services.ranks import get_rank

router = APIRouter(prefix="/api/auth", tags=["auth"])


def serialize_user(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        total_points=user.total_points,
        current_rank=get_rank(user.total_points),
        current_streak=user.current_streak,
        best_streak=user.best_streak,
        created_at=user.created_at,
    )


@router.post("/demo-login", response_model=UserResponse)
def demo_login(payload: DemoLoginRequest, session: Session = Depends(get_session)) -> UserResponse:
    username = payload.username.strip()
    if not username:
        raise HTTPException(status_code=422, detail="Username is required")

    user = session.scalar(select(User).where(User.username == username))
    if user is None:
        user = User(username=username)
        session.add(user)
        session.commit()
        session.refresh(user)
    return serialize_user(user)


@router.get("/me", response_model=UserResponse)
def get_me(
    user_id: int | None = Query(default=None),
    username: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> UserResponse:
    if user_id is None and username is None:
        raise HTTPException(status_code=400, detail="Provide user_id or username")

    statement = select(User).where(User.id == user_id) if user_id is not None else select(User).where(User.username == username)
    user = session.scalar(statement)
    if user is None:
        raise HTTPException(status_code=404, detail="Demo user not found")
    return serialize_user(user)
