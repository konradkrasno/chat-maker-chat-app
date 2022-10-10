from typing import Any, Dict, Iterable, List, Mapping, Union

from chat_app.exceptions import ItemDoesNotExistsError
from chat_app.models import Chat, User, UserChats, UserCreds


class AbstractRepo(dict):
    @classmethod
    def _base_load_from_dict(cls, data: Union[Dict, List], model: Any):
        obj = cls()
        if isinstance(data, Mapping):
            for k, v in data.items():
                obj[k] = model.load_from_dict(**v)
            return obj
        if isinstance(data, Iterable):
            for item in data:
                obj[item["id"]] = model.load_from_dict(**item)
            return obj
        raise Exception(f"Invalid data type: {type(data)}")

    def serialize(self) -> Dict:
        return {k: v.dict() for k, v in self.items()}

    def get_item(self, _id: str) -> Any:
        item = self.get(_id)
        if item:
            return item
        raise ItemDoesNotExistsError(f"Can not find item with provided id: '{_id}'.")

    def put_item(self, item: Dict) -> None:
        self[item["id"]] = item


class UserRepo(AbstractRepo):
    """
    Dict containing all users
        key: user id
        value: User object
    """

    @classmethod
    def load_from_dict(cls, data: List):
        return cls._base_load_from_dict(data, User)


class UserCredsRepo(AbstractRepo):
    """
    Dict containing hashed users credentials
        key: user id
        value: User credentials
    """

    @classmethod
    def load_from_dict(cls, data: List):
        return cls._base_load_from_dict(data, UserCreds)


class ChatRepo(AbstractRepo):
    """
    Dict containing all chats
        key: chat id
        value: Chat object
    """

    @classmethod
    def load_from_dict(cls, data: List):
        return cls._base_load_from_dict(data, Chat)


class UserChatsRepo(AbstractRepo):
    """
    Dict containing all user's chats ids
        key: user id
        value: UserChats object
    """

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserChats)

    def get_user_chats_ids(self, user_id: str) -> List[str]:
        user_chats = self.get_item(user_id)
        if user_chats:
            return user_chats.chat_ids
        return []
