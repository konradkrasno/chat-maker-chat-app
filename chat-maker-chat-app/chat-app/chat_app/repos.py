from typing import Any, Dict, List, Union

from chat_app.exceptions import ItemAlreadyExistsError, ItemDoesNotExistsError
from chat_app.models import Chat, Session, User, UserChats, UserCreds


class AbstractRepo(dict):
    repo_key = "id"
    unique_fields = [repo_key]

    @classmethod
    def _base_load_from_dict(cls, data: Dict, model: Any):
        obj = cls()
        for k, v in data.items():
            obj[k] = model.load_from_dict(**v)
        return obj

    def serialize(self) -> Dict:
        return {k: v.dict() for k, v in self.items()}

    def get_item(self, key: str) -> Any:
        item = self.get(key)
        if item:
            return item
        raise ItemDoesNotExistsError(f"Can not find item with provided key: '{key}'.")

    @classmethod
    def _get_key_from_item(cls, item: Any) -> Union[str, int]:
        return getattr(item, cls.repo_key)

    def put_item(self, item: Any) -> None:
        key = self._get_key_from_item(item)
        if key in self.keys():
            raise ItemAlreadyExistsError(f"Item with key: {key} already exists")
        for _obj in self.values():
            for field in self.unique_fields:
                f_v = getattr(item, field)
                if f_v == getattr(_obj, field):
                    raise ItemAlreadyExistsError(
                        f"{item.__class__.__name__} with field '{field}'='{f_v}' already exists"
                    )
        self[key] = item

    def update_item(self, item: Any) -> None:
        key = self._get_key_from_item(item)
        self[key] = item


class UserRepo(AbstractRepo):
    """
    Dict containing all users
        key: user id
        value: User object
    """

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, User)


class UserCredsRepo(AbstractRepo):
    """
    Dict containing hashed users credentials
        key: email
        value: User credentials
    """

    repo_key = "email"

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserCreds)


class SessionRepo(AbstractRepo):
    """
    Dict containing all sessions
        key: user id
        value: Chat object
    """

    repo_key = "user_id"

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, Session)


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

    repo_key = "user_id"

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserChats)

    def get_user_chats_ids(self, user_id: str) -> List[str]:
        user_chats = self.get_item(user_id)
        if user_chats:
            return user_chats.chat_ids
        return []
