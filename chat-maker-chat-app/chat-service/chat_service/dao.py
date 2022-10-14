from typing import Dict, List

from chat_service.models import Chat, Message
from chat_service.repos import ChatRepo, UserChatsRepo
from chat_service.settings import ApiSettings, get_api_settings
from fastapi import Depends
from user_service.models import User
from user_service.repos import UserRepo

from commons.dao import BaseDao
from commons.exceptions import ItemDoesNotExistsError


class ChatDao(BaseDao):
    def __init__(self, settings: ApiSettings = Depends(get_api_settings)):
        super().__init__(settings=settings)
        # TODO get rid of _users repo from this dao
        self._users = UserRepo.load_from_dict(self._load_data("users"))
        self._chats = ChatRepo.load_from_dict(self._load_data("chats"))
        self._users_chats = UserChatsRepo.load_from_dict(self._load_data("users_chats"))

    def _get_file_path(self, _type: str) -> str:
        super()._get_file_path(_type)
        file_path_map = {
            "users": "users.json",
            "chats": "chats.json",
            "users_chats": "users_chats.json",
        }
        return file_path_map[_type]

    def get_user_chats(self, user_id: str) -> List[Chat]:

        chat_ids = self._users_chats.get_user_chats_ids(user_id)
        return [self._chats[chat_id] for chat_id in chat_ids]

    def get_user_chat(self, user_id: str, chat_id: str) -> Chat:
        chat_ids = self._users_chats.get_user_chats_ids(user_id)
        if chat_id in chat_ids:
            return self._chats.get_item(chat_id)
        raise ItemDoesNotExistsError(
            f"Provided chat: '{chat_id}' does not exist or you are not permitted to join."
        )

    @staticmethod
    def _collect_member_info(member: User) -> Dict:
        return {
            **member.dict(),
            "active": True,
            "status": " ",
            "lastSeen": "online",
        }

    def get_chats_members_info(self, user_id: str) -> Dict[str, List]:
        chats = self.get_user_chats(user_id)
        return {
            chat.id: [
                self._collect_member_info(self._users.get_item(member_id))
                for member_id in chat.members
            ]
            for chat in chats
        }

    def put_message(self, user_id: str, chat_id: str, message_data: Dict) -> None:
        chat = self.get_user_chat(user_id, chat_id)
        message = Message.load_from_dict(**message_data)
        chat.add_message(message)
        self._dump_data("chats")


def get_chat_dao(settings: ApiSettings = Depends(get_api_settings)) -> ChatDao:
    return ChatDao(settings=settings)
