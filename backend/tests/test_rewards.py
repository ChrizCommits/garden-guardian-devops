from datetime import date, timedelta

from app import database
from app.models.user import User
from app.services.ranks import get_rank
from app.services.rewards import complete_tip
from app.services.seasonal_tips import get_tip_for_date


def _complete_current_tip(client, user_id: int):
    today = client.get("/api/today").json()
    response = client.post(f"/api/tips/{today['id']}/complete", json={"user_id": user_id})
    assert response.status_code == 200
    return today, response.json()


def test_completing_tip_awards_points(client, demo_user):
    _, completion = _complete_current_tip(client, demo_user["id"])

    assert completion["awarded"] is True
    assert completion["points_awarded"] == 1
    assert completion["total_points"] == 1
    assert completion["current_rank"] == "Tiny Helper"


def test_completing_tip_unlocks_matching_animal_card(client, demo_user):
    today, completion = _complete_current_tip(client, demo_user["id"])

    supported_names = {animal["name"] for animal in today["supported_animals"]}
    assert completion["unlocked_card"] is not None
    assert completion["unlocked_card"]["animal_name"] in supported_names


def test_completing_same_tip_twice_same_day_does_not_double_award(client, demo_user):
    today, first = _complete_current_tip(client, demo_user["id"])
    second_response = client.post(f"/api/tips/{today['id']}/complete", json={"user_id": demo_user["id"]})

    assert second_response.status_code == 200
    second = second_response.json()
    assert first["total_points"] == 1
    assert second["awarded"] is False
    assert second["points_awarded"] == 0
    assert second["total_points"] == 1


def test_rank_changes_correctly_at_thresholds():
    assert get_rank(0) == "Garden Visitor"
    assert get_rank(1) == "Tiny Helper"
    assert get_rank(2) == "Garden Friend"
    assert get_rank(5) == "Nature Ally"
    assert get_rank(10) == "Wildlife Guardian"
    assert get_rank(25) == "Habitat Hero"
    assert get_rank(50) == "Guardian of the Garden"


def test_streak_updates_correctly(client):
    session = database.SessionLocal()
    try:
        user = User(username="streakkeeper")
        session.add(user)
        session.commit()
        session.refresh(user)
        tip = get_tip_for_date(session)

        complete_tip(session, user, tip, date.today() - timedelta(days=1))
        assert user.current_streak == 1
        assert user.best_streak == 1

        complete_tip(session, user, tip, date.today())
        assert user.current_streak == 2
        assert user.best_streak == 2
    finally:
        session.close()
