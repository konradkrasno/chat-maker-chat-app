from typing import List
from uuid import uuid4

from commons.models import AbstractModel


class Message(AbstractModel):
    id: str
    sendDate: str
    content: str
    sender_id: str

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)


class Chat(AbstractModel):
    id: str
    members: List[str]
    messages: List[Message] = []

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(
            id=kwargs["id"],
            members=kwargs["members"],
            messages=[Message.load_from_dict(**item) for item in kwargs["messages"]],
        )

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    @classmethod
    def create_item(cls, members: List[str]) -> "Chat":
        _id = uuid4().hex
        return cls(id=_id, members=members)


class UserChats(AbstractModel):
    user_id: str
    chat_ids: List[str] = []

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(
            user_id=kwargs["user_id"],
            chat_ids=[chat_id for chat_id in kwargs["chat_ids"]],
        )

    @classmethod
    def create_item(cls, user_id: str) -> "UserChats":
        return cls(user_id=user_id)


class ChatMembers(AbstractModel):
    members_hash: str
    chat_id: str

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def create_item(cls, members_hash: str, chat_id: str) -> "ChatMembers":
        return cls(members_hash=members_hash, chat_id=chat_id)
