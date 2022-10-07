from chat_app.models import ChatModel, UserChatsModel, UserModel
from chat_app.schemas import Chat, User, UserChats


def test_user_model(dao):
    users_data = dao._load_data("users")
    user_model = UserModel.load_from_dict(users_data)
    assert isinstance(user_model, dict)
    assert isinstance(user_model["u1"], User)


def test_chat_model(dao):
    chats_data = dao._load_data("chats")
    chat_model = ChatModel.load_from_dict(chats_data)
    assert isinstance(chat_model, dict)
    assert isinstance(chat_model["chat2"], Chat)


def test_user_chats_model(dao):
    user_chats_data = dao._load_data("users_chats")
    user_chats_model = UserChatsModel.load_from_dict(user_chats_data)
    assert isinstance(user_chats_model, dict)
    assert isinstance(user_chats_model["u7"], UserChats)
