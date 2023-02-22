from unittest.mock import patch

from websocket_service.websocket.logic import manager


@patch("builtins.print")
def test_websocket_endpoint(
    mocked_print, websocket_1, websocket_2, mock_chat_service_client
):
    chat_id = "test-chat-id"
    assert websocket_1.receive_text() == "Client #test_user_1 joined the chat"
    assert websocket_1.receive_text() == "Client #test_user_2 joined the chat"
    assert websocket_2.receive_text() == "Client #test_user_2 joined the chat"
    assert len(manager.active_connections) == 2

    test_message_1 = {
        "message": {
            "id": "1",
            "sendDate": "test_time",
            "content": "test message 1",
            "sender_id": "test_user_1",
        },
        "chatId": chat_id,
    }
    websocket_1.send_json(test_message_1)

    assert websocket_1.receive_json() == test_message_1
    assert websocket_2.receive_json() == test_message_1
    mocked_print.assert_called_with("User #test_user_3 is inactive")
    mock_chat_service_client.put_message.assert_called_once_with(
        chat_id, test_message_1["message"]
    )
