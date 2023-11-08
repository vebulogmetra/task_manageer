import re

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
    assert response.status_code == test_status.success
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
    assert response.status_code == test_status.success
    assert len(response.json()) == 1


def test_upload_user_picture(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Upload file
    headers = {"accept": "application/json"} | auth_header
    picture_file = {"picture": open(test_const.test_image_filepath, "rb")}
    params = {"user_id": test_user.id}

    response = client.post(
        test_api.user_upload_picture,
        headers=headers,
        files=picture_file,
        params=params,
    )
    assert response.status_code == test_status.success

    # Try get user by id
    response = client.get(
        test_api.user_get,
        params={"by_field": "id", "by_value": test_user.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert isinstance(response.json()["avatar_url"], str)
    assert re.search(".png", response.json()["avatar_url"])


def test_update_user(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Update user last_name
    response = client.put(
        test_api.user_update,
        params={"user_id": test_user.id},
        headers=auth_header,
        json={"last_name": "Herber"},
    )
    assert response.status_code == test_status.success

    # Try get user by id
    response = client.get(
        test_api.user_get,
        params={"by_field": "id", "by_value": test_user.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert response.json()["last_name"] == "Herber"


def test_delete_user(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Delete user last_name
    response = client.delete(
        test_api.user_delete,
        params={"user_id": test_user.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success

    # Try get user by id
    response = client.get(
        test_api.user_get,
        params={"by_field": "id", "by_value": test_user.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.notfound
