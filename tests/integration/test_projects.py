from fastapi.testclient import TestClient

from tests.integration.resources import (
    test_api,
    test_const,
    test_project,
    test_status,
    test_user,
    test_user_developer,
)


def test_create_user(client: TestClient):
    # Create user
    response = client.post(test_api.user_create, json=test_user.to_dict())
    assert response.status_code == test_status.success

    user_id = str(response.json().get("id"))
    test_user.id = user_id
    test_project.creator_id = user_id


def test_create_project(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create project
    response = client.post(
        test_api.project_create,
        headers=auth_header,
        json=test_project.to_dict(),
    )
    assert response.status_code == test_status.success
    assert all(
        f in test_const.project_create_response_required_fields
        for f in response.json().keys()
    )
    assert response.json()["creator_id"] == test_user.id

    project_id = str(response.json().get("id"))
    test_project.id = project_id

    # Try get project by id
    response = client.get(
        test_api.project_get,
        params={"project_id": test_project.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success


def test_add_user_to_project(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create developer user
    response = client.post(test_api.user_create, json=test_user_developer.to_dict())
    assert response.status_code == test_status.success

    developer_id = str(response.json().get("id"))
    test_user_developer.id = developer_id

    # Add user to project
    response = client.post(
        test_api.project_add_user,
        headers=auth_header,
        json={"project_id": test_project.id, "user_id": developer_id},
    )
    assert response.status_code == test_status.success


def test_get_project(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Try get project by id (invalid id param)
    response = client.get(
        test_api.project_get,
        params={"project_id": "bad_project_id"},
        headers=auth_header,
    )
    assert response.status_code == test_status.invalid_input

    # Try get project by id (not found id)
    response = client.get(
        test_api.project_get,
        params={"project_id": "72dcf331-f537-41fc-8969-76492032c90d"},
        headers=auth_header,
    )
    assert response.status_code == test_status.notfound

    # Try get project by id
    response = client.get(
        test_api.project_get,
        params={"project_id": test_project.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert len(response.json()["users"]) == 1

    # Try get projects by owner
    response = client.get(test_api.projects_get_by_owner, headers=auth_header)
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["users"]) == 1

    # Try get projects
    response = client.get(
        test_api.projects_get, headers=auth_header, params={"limit": 5, "offset": 0}
    )
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["users"]) == 1


def test_update_project(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Update project name
    response = client.put(
        test_api.project_update,
        params={"project_id": test_project.id},
        headers=auth_header,
        json={"name": "HerberProject"},
    )
    assert response.status_code == test_status.success

    # Try get project by id
    response = client.get(
        test_api.project_get,
        params={"project_id": test_project.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert response.json()["name"] == "HerberProject"


def test_delete_project(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Delete project
    response = client.delete(
        test_api.project_delete,
        params={"project_id": test_project.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success

    # Try get project by id
    response = client.get(
        test_api.project_get,
        params={"project_id": test_project.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.notfound
