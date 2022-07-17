def test_load_users(dao):
    assert len(dao._users) == 7


def test_load_chats(dao):
    assert len(dao._chats) == 6
    assert dao._chats["chat2"].id == "chat2"
    assert len(dao._chats["chat2"].messages) == 3


def test_load_users_chats(dao):
    assert len(dao._users_chats) == 1


def test_get_user_chat(dao):
    assert dao.get_user_chat("u7", "chat2") == dao._chats["chat2"]
