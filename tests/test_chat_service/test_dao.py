def test_load_chats(chat_dao):
    assert len(chat_dao._chats) == 6
    assert chat_dao._chats["chat2"].id == "chat2"
    assert len(chat_dao._chats["chat2"].messages) == 3


def test_load_users_chats(chat_dao):
    assert len(chat_dao._users_chats) == 1


def test_get_user_chat(chat_dao, user_id):
    assert chat_dao.get_user_chat(user_id, "chat2") == chat_dao._chats["chat2"]
