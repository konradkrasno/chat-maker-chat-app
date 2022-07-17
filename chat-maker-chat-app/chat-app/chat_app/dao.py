import json
from pathlib import Path
from typing import Dict, List

from chat_app.schemas import Chat
from chat_app.models import ChatModel, UserModel, UserChatsModel
from chat_app.exceptions import ChatDoesNotExistsError

BASE_DIR = Path(__name__).resolve().parent
DATA_DIR = BASE_DIR / "data"


class Dao:
    def __init__(self, storage_type: str):
        self.__storage_type = storage_type

    def _load_data(self, _type: str) -> Dict:
        if self.__storage_type == "files":
            file_path_map = {
                "users": "users.json",
                "chats": "chats.json",
                "users_chats": "users_chats.json",
            }
            file_path = file_path_map[_type]
            with open(DATA_DIR / file_path) as file:
                return json.load(file)
        return {}

    @property
    def users(self) -> UserModel:
        data = self._load_data("users")
        return UserModel.load_from_dict(data)

    @property
    def chats(self) -> ChatModel:
        data = self._load_data("chats")
        return ChatModel.load_from_dict(data)

    @property
    def users_chats(self) -> UserChatsModel:
        data = self._load_data("users_chats")
        return UserChatsModel.load_from_dict(data)

    def get_user_chats(self, user_id: str) -> List[Chat]:
        chat_ids = self.users_chats.get_user_chats_ids(user_id)
        return [self.chats[chat_id] for chat_id in chat_ids]

    def get_user_chat(self, user_id: str, chat_id: str) -> Chat:
        chat_ids = self.users_chats.get_user_chats_ids(user_id)
        if chat_id in chat_ids:
            return self.chats.get_chat(chat_id)
        raise ChatDoesNotExistsError(
            f"Provided chat: '{chat_id}' does not exist or you are not permitted to join."
        )
