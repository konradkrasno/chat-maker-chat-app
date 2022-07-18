import json
from pathlib import Path
from typing import Dict, List, Union

from chat_app.schemas import Chat, Message, User
from chat_app.models import ChatModel, UserModel, UserChatsModel
from chat_app.exceptions import ItemDoesNotExistsError

BASE_DIR = Path(__name__).resolve().parent
DATA_DIR = BASE_DIR / "data"


class Dao:
    def __init__(self, storage_type: str):
        self.__storage_type = storage_type
        self._users = UserModel.load_from_dict(self._load_data("users"))
        self._chats = ChatModel.load_from_dict(self._load_data("chats"))
        self._users_chats = UserChatsModel.load_from_dict(
            self._load_data("users_chats")
        )

    @staticmethod
    def _get_file_path(_type: str) -> str:
        file_path_map = {
            "users": "users.json",
            "chats": "chats.json",
            "users_chats": "users_chats.json",
        }
        return file_path_map[_type]

    def _load_data(self, _type: str) -> Union[Dict, List]:
        if self.__storage_type == "files":
            file_path = self._get_file_path(_type)
            with open(DATA_DIR / file_path, "r") as file:
                return json.load(file)
        return {}

    def _dump_data(self, _type: str) -> None:
        if self.__storage_type == "files":
            file_path = self._get_file_path(_type)
            with open(DATA_DIR / file_path, "w") as file:
                return json.dump(self.__getattribute__(f"_{_type}").serialize(), file)

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
    def collect_member_info(member: User, chat_id: str) -> Dict:
        return {
            **member.dict(),
            "chat_id": chat_id,
            "active": True,
            "status": " ",
            "lastSeen": "online",
        }

    def get_chats_members_info(self, user_id: str) -> List[Dict]:
        chats = self.get_user_chats(user_id)
        members_info = []
        for chat in chats:
            members_ids = chat.members
            for member_id in members_ids:
                member = self._users.get_item(member_id)
                info = self.collect_member_info(member, chat.id)
                members_info.append(info)
        return members_info

    def put_message(self, user_id: str, chat_id: str, message_data: Dict) -> None:
        chat = self.get_user_chat(user_id, chat_id)
        message = Message.load_from_dict(**message_data)
        chat.add_message(message)
        self._dump_data("chats")
