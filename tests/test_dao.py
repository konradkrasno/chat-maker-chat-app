def test_load_users(dao):
    assert len(dao.users) == 6


def test_load_chats(dao):
    assert len(dao.chats) == 1
    assert dao.chats["11AA1CA0E120450"].id == "11AA1CA0E120450"
    assert len(dao.chats["11AA1CA0E120450"].messages) == 3


def test_load_users_chats(dao):
    assert len(dao.users_chats) == 1
    assert dao.users_chats["u7"].chat_ids == ["11AA1CA0E120450"]


def test_get_user_chat(dao):
    assert dao.get_user_chat("u7", "11AA1CA0E120450") == dao.chats["11AA1CA0E120450"]
