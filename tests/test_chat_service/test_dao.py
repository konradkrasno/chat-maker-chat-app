from commons.repos import AbstractRepo


def test_load_chats(chat_dao, chat_id):
    assert isinstance(chat_dao._chats, AbstractRepo)
    assert chat_dao._chats
    assert chat_dao._chats[chat_id].id == chat_id
    assert chat_dao._chats[chat_id].messages


def test_load_users_chats(chat_dao):
    assert isinstance(chat_dao._users_chats, AbstractRepo)
    assert chat_dao._users_chats


def test_get_user_chat(chat_dao, chat_id):
    assert chat_dao.get_user_chat(chat_id) == chat_dao._chats[chat_id]
