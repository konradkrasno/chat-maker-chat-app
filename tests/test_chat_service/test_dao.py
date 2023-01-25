import pytest
from commons.repos import AbstractRepo


def test_load_chats(chat_dao, chat_id):
    assert isinstance(chat_dao._chats, AbstractRepo)
    assert chat_dao._chats
    assert chat_dao._chats[chat_id].id == chat_id
    assert chat_dao._chats[chat_id].messages


def test_load_users_chats(chat_dao):
    assert isinstance(chat_dao._users_chats, AbstractRepo)
    assert chat_dao._users_chats


@pytest.mark.asyncio
async def test_get_user_chat(chat_dao, chat_id):
    chat = await chat_dao.get_user_chat(chat_id)
    expected_chat = chat_dao._chats[chat_id]
    assert chat["id"] == expected_chat.id
    assert chat["members"] == expected_chat.members
    assert chat["messages"][0]["id"] == expected_chat.messages[0].id
    assert "sender" in chat["messages"][0]
