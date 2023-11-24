from fastapi.testclient import TestClient

from tests.integration.resources import (
    test_api,
    test_chat,
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

    # Create developer user
    response = client.post(test_api.user_create, json=test_user_developer.to_dict())
    assert response.status_code == test_status.success

    developer_id = str(response.json().get("id"))
    test_user_developer.id = developer_id
    test_chat.interlocutor_id = developer_id


def test_create_dialog(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Create dialog
    response = client.post(
        test_api.chat_create,
        headers=auth_header,
        json=test_chat.to_dict(),
    )
    assert response.status_code == test_status.success
    dialog_id = str(response.json().get("id"))
    test_chat.id = dialog_id


def test_add_message(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}
    # Add message without sender_id
    response = client.post(
        test_api.chat_add_message,
        headers=auth_header,
        json={"dialog_id": test_chat.id, "content": "test message 1"},
    )
    assert response.status_code == test_status.success
    # Add message with sender id
    response = client.post(
        test_api.chat_add_message,
        headers=auth_header,
        json={
            "dialog_id": test_chat.id,
            "sender_id": test_user_developer.id,
            "content": "test message 2",
        },
    )
    assert response.status_code == test_status.success


def test_get_chat(client: TestClient, access_token):
    auth_header = {"Authorization": f"bearer {access_token}"}

    # Try get chat by id (invalid id param)
    response = client.get(
        test_api.chat_get,
        params={"dialog_id": "bad__id"},
        headers=auth_header,
    )
    assert response.status_code == test_status.invalid_input

    # Try get chat by id (not found id)
    response = client.get(
        test_api.chat_get,
        params={"dialog_id": "72dcf331-f537-41fc-8969-99999099c90d"},
        headers=auth_header,
    )
    assert response.status_code == test_status.notfound

    # Try get dialog by id
    response = client.get(
        test_api.chat_get,
        params={"dialog_id": test_chat.id},
        headers=auth_header,
    )
    assert response.status_code == test_status.success
    assert len(response.json()["messages"]) == 2

    # Try get dialog by creator
    response = client.get(test_api.chats_by_creator_get, headers=auth_header)
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["messages"]) == 2

    # Try get dialog by interlocutor
    response = client.get(
        test_api.chats_by_interlocutor_get,
        headers=auth_header,
        params={"interlocutor_id": test_user_developer.id},
    )
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["messages"]) == 2

    # Try get chats
    response = client.get(
        test_api.chats_get, headers=auth_header, params={"limit": 5, "offset": 0}
    )
    assert response.status_code == test_status.success
    assert len(response.json()) == 1
    assert len(response.json()[0]["messages"]) == 2
