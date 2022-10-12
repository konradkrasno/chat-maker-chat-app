from typing import Any, Dict, Iterable, List, Mapping, Union

from chat_app.exceptions import ItemAlreadyExistsError, ItemDoesNotExistsError
from chat_app.models import Chat, User, UserChats, UserCreds


class AbstractRepo(dict):
    repo_key = "id"
    unique_fields = []

    @classmethod
    def _base_load_from_dict(cls, data: Dict, model: Any):
        obj = cls()
        for k, v in data.items():
            obj[k] = model.load_from_dict(**v)
        return obj

    def serialize(self) -> Dict:
        return {k: v.dict() for k, v in self.items()}

    def get_item(self, _id: str) -> Any:
        item = self.get(_id)
        if item:
            return item
        raise ItemDoesNotExistsError(f"Can not find item with provided id: '{_id}'.")

    def put_item(self, item: Any) -> None:
        if item.id in self.keys():
            raise ItemAlreadyExistsError(f"Item with id: {item.id} already exists")
        for _obj in self.values():
            for field in self.unique_fields:
                f_v = getattr(item, field)
                if f_v == getattr(_obj, field):
                    raise ItemAlreadyExistsError(
                        f"{item.__class__.__name__} with field '{field}'='{f_v}' already exists"
                    )
        repo_key = getattr(item, self.repo_key)
        self[repo_key] = item


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
        key: user id
        value: User credentials
    """

    repo_key = "email"
    unique_fields = ["email"]

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserCreds)


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

    @classmethod
    def load_from_dict(cls, data: Dict):
        return cls._base_load_from_dict(data, UserChats)

    def get_user_chats_ids(self, user_id: str) -> List[str]:
        user_chats = self.get_item(user_id)
        if user_chats:
            return user_chats.chat_ids
        return []
