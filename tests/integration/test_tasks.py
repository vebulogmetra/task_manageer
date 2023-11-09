from fastapi.testclient import TestClient

from tests.integration.resources import (
    test_api,
    test_project,
    test_status,
    test_task,
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
    test_task.creator_id = user_id


def test_create_project(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create project
    response = client.post(
        test_api.project_create,
        headers=auth_header,
        json=test_project.to_dict(),
    )
    assert response.status_code == test_status.success

    project_id = str(response.json().get("id"))
    test_project.id = project_id
    test_task.project_id = project_id


def test_create_task(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create task
    response = client.post(
        test_api.task_create,
        headers=auth_header,
        json=test_task.to_dict(),
    )
    assert response.status_code == test_status.success
    assert response.json()["creator_id"] == test_user.id

    task_id = str(response.json().get("id"))
    test_task.id = task_id

    # Try get task by id
    response = client.get(
        test_api.task_get,
        params={"task_id": test_task.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success


def test_add_user_to_task(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create developer user
    response = client.post(test_api.user_create, json=test_user_developer.to_dict())
    assert response.status_code == test_status.success

    developer_id = str(response.json().get("id"))
    test_user_developer.id = developer_id

    # Add user to task
    response = client.post(
        test_api.task_add_user,
        headers=auth_header,
        json={"task_id": test_task.id, "user_id": developer_id},
    )
    assert response.status_code == test_status.success


def test_get_task(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Try get task by id (invalid id param)
    response = client.get(
        test_api.task_get,
        params={"task_id": "bad_task_id"},
        headers=auth_header,
    )
    assert response.status_code == test_status.invalid_input

    # Try get task by id (not found id)
    response = client.get(
        test_api.task_get,
        params={"task_id": "72dcf331-f537-41fc-8969-76492032c90d"},
        headers=auth_header,
    )
    assert response.status_code == test_status.notfound

    # Try get task by id
    response = client.get(
        test_api.task_get,
        params={"task_id": test_task.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert len(response.json()["users"]) == 1

    # Try get task by owner
    response = client.get(test_api.tasks_get_by_owner, headers=auth_header)
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["users"]) == 1

    # Try get tasks
    response = client.get(
        test_api.tasks_get, headers=auth_header, params={"limit": 5, "offset": 0}
    )
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["users"]) == 1


def test_update_task(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Update task name
    response = client.put(
        test_api.task_update,
        params={"task_id": test_task.id},
        headers=auth_header,
        json={"title": "HerberTask"},
    )
    assert response.status_code == test_status.success

    # Try get task by id
    response = client.get(
        test_api.task_get,
        params={"task_id": test_task.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert response.json()["title"] == "HerberTask"


def test_delete_task(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Delete task
    response = client.delete(
        test_api.task_delete,
        params={"task_id": test_task.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success

    # Try get task by id
    response = client.get(
        test_api.task_get,
        params={"task_id": test_task.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.notfound
