def test_load_users(chat_dao):
    assert len(chat_dao._users) == 7


def test_load_chats(chat_dao):
    assert len(chat_dao._chats) == 6
    assert chat_dao._chats["chat2"].id == "chat2"
    assert len(chat_dao._chats["chat2"].messages) == 3


def test_load_users_chats(chat_dao):
    assert len(chat_dao._users_chats) == 1


def test_get_user_chat(chat_dao):
    assert chat_dao.get_user_chat("u7", "chat2") == chat_dao._chats["chat2"]
