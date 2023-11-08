from fastapi.testclient import TestClient

from tests.integration.resources import test_api, test_const, test_status, test_user


def test_create_user(client: TestClient):
    # Create user
    response = client.post(test_api.user_create, json=test_user.to_dict())
    assert response.status_code == test_status.success

    user_id = str(response.json().get("id"))
    test_user.id = user_id

    # Try user login
    response = client.post(
        "/api/v1/auth/login",
        headers=test_const.user_login_headers,
        data={"username": test_user.email, "password": test_user.password},
    )
    assert response.status_code == 200
    assert all(f in test_const.user_login_require_fields for f in response.json().keys())
    assert response.json()["token_type"] == "bearer"


def test_get_user(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Try get user by id
    response = client.get(
        test_api.user_get,
        params={"by_field": "id", "by_value": test_user.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert response.json()["email"] == test_user.email

    # Try get users
    response = client.get(test_api.users_get, headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) == 1
