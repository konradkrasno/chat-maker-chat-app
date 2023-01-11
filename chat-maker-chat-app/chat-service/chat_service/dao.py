from typing import Dict, List, Set

from chat_service.models import Chat, ChatMembers, Message
from chat_service.repos import ChatMembersRepo, ChatRepo, UserChatsRepo
from chat_service.settings import ApiSettings, get_api_settings
from commons.clients import UserServiceClient, get_user_service_client
from commons.dao import BaseDao
from commons.exceptions import ItemDoesNotExistsError
from commons.utils import hash_set
from fastapi import Depends
from user_service.models import User


class ChatDao(BaseDao):
    def __init__(
        self,
        user_id: str,
        settings: ApiSettings = Depends(get_api_settings),
        user_service_client: UserServiceClient = Depends(get_user_service_client),
    ):
        super().__init__(settings=settings)
        self._user_id = user_id
        self._chats = ChatRepo.load_from_dict(self._load_data("chats"))
        self._users_chats = UserChatsRepo.load_from_dict(self._load_data("users_chats"))
        self._chat_members = ChatMembersRepo.load_from_dict(
            self._load_data("chat_members")
        )
        self._user_service_client = user_service_client

    def _get_file_path(self, _type: str) -> str:
        super()._get_file_path(_type)
        file_path_map = {
            "chats": "chats.json",
            "users_chats": "users_chats.json",
            "chat_members": "chat_members.json",
        }
        return file_path_map[_type]

    def get_user_chats(self) -> List[Chat]:
        chat_ids = self._users_chats.get_or_create_user_chats(self._user_id)
        return [self._chats[chat_id] for chat_id in chat_ids]

    def get_user_chat(self, chat_id: str) -> Chat:
        chat_ids = self._users_chats.get_or_create_user_chats(self._user_id)
        if chat_id in chat_ids:
            return self._chats.get_item(chat_id)
        raise ItemDoesNotExistsError(
            f"Provided chat: '{chat_id}' does not exist or you have no access."
        )

    def _prepare_member_ids(self, member_ids: List[str]) -> Set[str]:
        member_ids.append(self._user_id)
        return set(member_ids)

    def get_chat_by_user(self, member_ids: List[str]) -> Chat:
        member_ids_set = self._prepare_member_ids(member_ids=member_ids)
        members_hash = hash_set(member_ids_set)
        try:
            chat_members = self._chat_members.get_item(members_hash)
        except ItemDoesNotExistsError:
            return self.create_chat(member_ids)
        return self._chats.get_item(chat_members.chat_id)

    async def get_chats_members_info(self) -> Dict[str, List[User]]:
        chats = self.get_user_chats()
        return {
            chat.id: [
                User.load_from_dict(**member)
                for member in await self._user_service_client.get_users_by_ids(
                    query_ids=list(chat.members)
                    # TODO add exception for chat with oneself
                )
                if member["id"] != self._user_id
            ]
            for chat in chats
        }

    def create_chat(self, member_ids: List[str]) -> Chat:
        chat = Chat.create_item(member_ids)
        self._chats.put_item(chat)
        chat_members = ChatMembers.create_item(
            members_hash=hash_set(set(member_ids)), chat_id=chat.id
        )
        self._chat_members.put_item(chat_members)
        for _id in member_ids:
            self._users_chats.get_or_create_user_chats(_id).append(chat.id)
        self._dump_data("chats")
        self._dump_data("chat_members")
        self._dump_data("users_chats")
        return chat

    def put_message(self, chat_id: str, message_data: Dict) -> None:
        chat = self.get_user_chat(chat_id)
        message = Message.load_from_dict(**message_data)
        chat.add_message(message)
        self._dump_data("chats")


def get_chat_dao(
    user_id: str,
    settings: ApiSettings = Depends(get_api_settings),
    user_service_client: UserServiceClient = Depends(get_user_service_client),
) -> ChatDao:
    return ChatDao(
        user_id=user_id, settings=settings, user_service_client=user_service_client
    )
