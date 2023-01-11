from typing import Dict, List

from chat_service.models import Chat, ChatMembers, UserChats
from commons.exceptions import ItemDoesNotExistsError
from commons.repos import AbstractRepo


class ChatRepo(AbstractRepo):
    """
    Dict containing all chats
        key: chat id
        value: Chat object
    """

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, Chat)


class UserChatsRepo(AbstractRepo):
    """
    Dict containing all user's chats ids
        key: user id
        value: UserChats object
    """

    repo_key = ("user_id",)
    unique_fields = ("user_id",)

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserChats)

    def get_or_create_user_chats(self, user_id: str) -> List[str]:
        try:
            user_chats = self.get_item(user_id)
        except ItemDoesNotExistsError:
            user_chats = UserChats.create_item(user_id)
            self.put_item(user_chats)
        return user_chats.chat_ids


class ChatMembersRepo(AbstractRepo):
    """
    Dict containing all chats owned by specified list of members converted to hash value
        key: members hash
        value: Chat object
    """

    repo_key = ("members_hash",)
    unique_fields = ("members_hash",)

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, ChatMembers)
