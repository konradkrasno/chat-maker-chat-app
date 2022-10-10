import json
from abc import ABC, abstractmethod
from typing import Dict, List, Union
from uuid import uuid4

from _sha1 import sha1
from chat_app.exceptions import ItemDoesNotExistsError
from chat_app.models import Chat, Message, User, UserCreds
from chat_app.repos import ChatRepo, UserChatsRepo, UserCredsRepo, UserRepo
from chat_app.settings import ApiSettings, get_api_settings
from fastapi import Depends


class BaseDao(ABC):
    def __init__(self, settings: ApiSettings = Depends(get_api_settings)):
        self.__storage_type = settings.STORAGE_TYPE
        self._settings = settings

    @abstractmethod
    def _get_file_path(self, _type: str) -> str:
        pass

    def _load_data(self, _type: str) -> Union[Dict, List]:
        if self.__storage_type == "files":
            file_path = self._get_file_path(_type)
            with open(self._settings.DATA_DIR / file_path, "r") as file:
                return json.load(file)
        return {}

    def _dump_data(self, _type: str) -> None:
        if self.__storage_type == "files":
            file_path = self._get_file_path(_type)
            with open(self._settings.DATA_DIR / file_path, "w") as file:
                return json.dump(self.__getattribute__(f"_{_type}").serialize(), file)


class UserDao(BaseDao):
    def __init__(self, settings: ApiSettings = Depends(get_api_settings)):
        super().__init__(settings=settings)
        self._users = UserRepo.load_from_dict(self._load_data("users"))
        self._user_creds = UserCredsRepo.load_from_dict(self._load_data("user_creds"))

    def _get_file_path(self, _type: str) -> str:
        super()._get_file_path(_type)
        file_path_map = {
            "users": "users.json",
        }
        return file_path_map[_type]

    def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        avatar_source: str = "",
    ):
        user_id = uuid4()
        user = User(id=user_id, name=name, surname=surname, avatar_source=avatar_source)
        user_creds = UserCreds(
            email=email,
            password=sha1(password),
        )
        self._users.put_item(user)
        self._user_creds.put_item(user_creds)
        self._dump_data("users")
        self._dump_data("user_creds")

    def login(self, email: str, password: str):
        pass

    def logout(self, user_id: str):
        pass


class ChatDao(BaseDao):
    def __init__(self, settings: ApiSettings = Depends(get_api_settings)):
        super().__init__(settings=settings)
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


def get_user_dao(settings: ApiSettings = Depends(get_api_settings)) -> UserDao:
    return UserDao(settings=settings)


def get_chats_dao(settings: ApiSettings = Depends(get_api_settings)) -> ChatDao:
    return ChatDao(settings=settings)
