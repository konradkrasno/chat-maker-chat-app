from chat_service.models import Chat, UserChats
from chat_service.repos import ChatRepo, UserChatsRepo
from commons.repos import AbstractRepo


def test_chat_repo(chat_dao, chat_id):
    chats_data = chat_dao._load_data("chats")
    chat_model = ChatRepo.load_from_dict(chats_data)
    assert isinstance(chat_model, AbstractRepo)
    assert isinstance(chat_model[chat_id], Chat)


def test_user_chats_repo(chat_dao, user_id):
    user_chats_data = chat_dao._load_data("users_chats")
    user_chats_model = UserChatsRepo.load_from_dict(user_chats_data)
    assert isinstance(user_chats_model, AbstractRepo)
    assert isinstance(user_chats_model[user_id], UserChats)
