def test_profile_returns_collected_cards(client, demo_user):
    today = client.get("/api/today").json()
    complete_response = client.post(f"/api/tips/{today['id']}/complete", json={"user_id": demo_user["id"]})
    assert complete_response.status_code == 200

    response = client.get("/api/profile", params={"user_id": demo_user["id"]})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == demo_user["username"]
    assert data["collected_cards"]
    assert data["recent_actions"]
    assert data["favorite_animals"]


def test_cards_endpoint_returns_collected_cards(client, demo_user):
    today = client.get("/api/today").json()
    client.post(f"/api/tips/{today['id']}/complete", json={"user_id": demo_user["id"]})

    response = client.get("/api/cards", params={"user_id": demo_user["id"]})

    assert response.status_code == 200
    assert response.json()["cards"]
