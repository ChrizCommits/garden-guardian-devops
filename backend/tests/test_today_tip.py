def test_today_tip_returns_valid_data(client):
    response = client.get("/api/today")

    assert response.status_code == 200
    data = response.json()
    assert data["title"]
    assert data["action_instruction"]
    assert data["points_reward"] > 0
    assert data["supported_animals"]
    assert data["possible_reward_cards"]


def test_unsafe_foods_are_included_in_warnings(client):
    response = client.get("/api/today")

    assert response.status_code == 200
    warning = response.json()["safety_warning"].lower()
    assert "milk" in warning
    assert "bread" in warning
    assert "chocolate" in warning
    assert "honey water" in warning
    assert "veterinary" not in warning
