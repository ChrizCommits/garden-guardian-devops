from collections.abc import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


Base = declarative_base()


def _database_url() -> str:
    return os.getenv("GARDENGUARDIAN_DATABASE_URL", "sqlite:///./gardenguardian.db")


def _connect_args(database_url: str) -> dict[str, bool]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(_database_url(), connect_args=_connect_args(_database_url()))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def configure_database(database_url: str) -> None:
    global engine, SessionLocal

    engine = create_engine(database_url, connect_args=_connect_args(database_url))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    from app.models.action import CompletedAction, UserAnimalCard  # noqa: F401
    from app.models.animal import Animal  # noqa: F401
    from app.models.card import AnimalCard  # noqa: F401
    from app.models.tip import DailyTip  # noqa: F401
    from app.models.user import User  # noqa: F401
    from app.services.seasonal_tips import seed_sample_data

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed_sample_data(session)
    finally:
        session.close()
