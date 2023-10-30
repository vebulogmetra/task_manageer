def test_create_user(client):
    response = client.get("/api/v1/users/users")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post(
        "/api/v1/users/create",
        json={"username": "fedor", "password": "qwerty"},
    )
    assert response.status_code == 200

    response = client.get(f"/api/v1/users/user/{response.json().get('id')}")
    assert response.status_code == 200
    assert response.json()["created_at"]

    response = client.get("/api/v1/users/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
