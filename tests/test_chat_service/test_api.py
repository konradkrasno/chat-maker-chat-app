from unittest.mock import MagicMock


def test_get_user_chats_when_200(test_user_id, chat_service_client):
    response = chat_service_client.get(f"/chats/{test_user_id}")
    assert response.status_code == 200
    assert response.json() == {}


def test_get_user_chats_when_401(
    test_user_id, chat_service_client, mock_auth_service_client
):
    mock_auth_service_client.authenticate = MagicMock(return_value=False)
    response = chat_service_client.get(f"/chats/{test_user_id}", headers={})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized token."}
