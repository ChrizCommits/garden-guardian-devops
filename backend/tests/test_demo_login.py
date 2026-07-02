def test_demo_user_can_be_created_with_username(client):
    response = client.post("/api/auth/demo-login", json={"username": "leaf"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "leaf"
    assert data["total_points"] == 0
    assert data["current_rank"] == "Garden Visitor"


def test_existing_demo_user_can_be_loaded_again(client):
    first = client.post("/api/auth/demo-login", json={"username": "fern"}).json()
    second = client.post("/api/auth/demo-login", json={"username": "fern"}).json()

    assert second["id"] == first["id"]
    assert second["username"] == "fern"
