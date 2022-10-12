from chat_app.models import Chat, User, UserChats
from chat_app.repos import ChatRepo, UserChatsRepo, UserRepo


def test_user_repo(chat_dao):
    users_data = chat_dao._load_data("users")
    user_model = UserRepo.load_from_dict(users_data)
    assert isinstance(user_model, dict)
    assert isinstance(user_model["u1"], User)


def test_chat_repo(chat_dao):
    chats_data = chat_dao._load_data("chats")
    chat_model = ChatRepo.load_from_dict(chats_data)
    assert isinstance(chat_model, dict)
    assert isinstance(chat_model["chat2"], Chat)


def test_user_chats_repo(chat_dao):
    user_chats_data = chat_dao._load_data("users_chats")
    user_chats_model = UserChatsRepo.load_from_dict(user_chats_data)
    assert isinstance(user_chats_model, dict)
    assert isinstance(user_chats_model["u7"], UserChats)
