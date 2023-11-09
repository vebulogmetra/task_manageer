from fastapi.testclient import TestClient

from tests.integration.resources import (
    test_api,
    test_status,
    test_team,
    test_user,
    test_user_developer,
)


def test_create_user(client: TestClient):
    # Create user
    response = client.post(test_api.user_create, json=test_user.to_dict())
    assert response.status_code == test_status.success

    user_id = str(response.json().get("id"))
    test_user.id = user_id
    test_team.creator_id = user_id


def test_create_team(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create team
    response = client.post(
        test_api.team_create,
        headers=auth_header,
        json=test_team.to_dict(),
    )
    assert response.status_code == test_status.success
    assert response.json()["creator_id"] == test_user.id

    team_id = str(response.json().get("id"))
    test_team.id = team_id

    # Try get team by id
    response = client.get(
        test_api.team_get,
        params={"team_id": test_team.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success


def test_add_user_to_team(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create developer user
    response = client.post(test_api.user_create, json=test_user_developer.to_dict())
    assert response.status_code == test_status.success

    developer_id = str(response.json().get("id"))
    test_user_developer.id = developer_id

    # Add user to team
    response = client.post(
        test_api.team_add_user,
        headers=auth_header,
        json={"team_id": test_team.id, "user_id": developer_id},
    )
    assert response.status_code == test_status.success


def test_get_team(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Try get team by id (invalid id param)
    response = client.get(
        test_api.team_get,
        params={"team_id": "bad_team_id"},
        headers=auth_header,
    )
    assert response.status_code == test_status.invalid_input

    # # Try get team by id (not found id)
    # response = client.get(
    #     test_api.team_get,
    #     params={"team_id": "5fdd6573-1808-4802-bc4e-8de082d472a7"},
    #     headers=auth_header,
    # )
    # assert response.status_code == test_status.notfound

    # Try get team by id
    response = client.get(
        test_api.team_get,
        params={"team_id": test_team.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert len(response.json()["users"]) == 1

    # Try get teams
    response = client.get(
        test_api.teams_get, headers=auth_header, params={"limit": 5, "offset": 0}
    )
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["users"]) == 1


def test_update_team(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Update team name
    response = client.put(
        test_api.team_update,
        params={"team_id": test_team.id},
        headers=auth_header,
        json={"title": "HerberTeam"},
    )
    assert response.status_code == test_status.success

    # Try get team by id
    response = client.get(
        test_api.team_get,
        params={"team_id": test_team.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert response.json()["title"] == "HerberTeam"


def test_delete_team(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Delete team
    response = client.delete(
        test_api.team_delete,
        params={"team_id": test_team.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success

    # # Try get team by id
    # response = client.get(
    #     test_api.team_get,
    #     params={"team_id": test_team.id},
    #     headers=auth_header,
    # )
    # assert response.status_code == test_status.notfound
