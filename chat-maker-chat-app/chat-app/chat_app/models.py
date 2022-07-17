from abc import abstractmethod
from typing import Dict, List, Union

from chat_app.schemas import Chat, User, UserChats
from chat_app.exceptions import ChatDoesNotExistsError

# chat_id = uuid.uuid4().hex[:10].upper()


class AbstractModel(dict):
    @classmethod
    @abstractmethod
    def load_from_dict(cls, data: Union[Dict, List]):
        pass

    def serialize(self) -> Dict:
        return {k: v.dict() for k, v in self.items()}


class UserModel(AbstractModel):
    """
    Dict containing all users
        key: user id
        value: User object
    """

    @classmethod
    def load_from_dict(cls, data: List):
        obj = cls()
        for item in data:
            obj[item["id"]] = User.load_from_dict(**item)
        return obj


class ChatModel(AbstractModel):
    """
    Dict containing all chats
        key: chat id
        value: Chat object
    """

    @classmethod
    def load_from_dict(cls, data: Dict):
        obj = cls()
        for k, v in data.items():
            obj[k] = Chat.load_from_dict(**v)
        return obj

    def get_chat(self, chat_id: str) -> Chat:
        chat = self.get(chat_id)
        if chat:
            return chat
        raise ChatDoesNotExistsError(
            f"Can not find chat with provided id: '{chat_id}'."
        )


class UserChatsModel(AbstractModel):
    """
    Dict containing all user's chats ids
        key: user id
        value: UserChats object
    """

    @classmethod
    def load_from_dict(cls, data: Dict):
        obj = cls()
        for k, v in data.items():
            obj[k] = UserChats.load_from_dict(user_id=k, chat_ids=v)
        return obj

    def get_user_chats_ids(self, user_id: str) -> List[str]:
        user_chats = self.get(user_id)
        if user_chats:
            return user_chats.chat_ids
        return []
