from hashlib import sha256
from typing import List
from uuid import uuid4

from pydantic import BaseModel


class User(BaseModel):
    id: str
    avatarSource: str
    name: str
    surname: str

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)


class UserCreds(BaseModel):
    id: str
    email: str
    password: str
    _salt: str

    @classmethod
    def load_from_dict(cls, **kwargs):
        salt = cls._get_salt()
        return cls(
            id=kwargs["id"],
            email=kwargs["email"],
            password=cls._hash_password(kwargs["password"], salt),
            _salt=salt,
        )

    @staticmethod
    def _get_salt() -> str:
        return uuid4().hex[:6]

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        salted_password = f"{salt}{password}"
        return sha256(salted_password.encode()).hexdigest()

    # def check_password(self, password: str):
    #     unhashed = sha256(self.password).digest()


class Message(BaseModel):
    id: str
    sendDate: str
    content: str
    sender: User

    @classmethod
    def load_from_dict(cls, **kwargs):
        kwargs["sender"] = User(**kwargs["sender"])
        return cls(**kwargs)


class Chat(BaseModel):
    id: str
    members: List[str]
    messages: List[Message]

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(
            id=kwargs["id"],
            members=kwargs["members"],
            messages=[Message.load_from_dict(**item) for item in kwargs["messages"]],
        )

    def add_message(self, message: Message) -> None:
        self.messages.append(message)


class UserChats(BaseModel):
    user_id: str
    chat_ids: List[str]

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(
            user_id=kwargs["user_id"],
            chat_ids=[chat_id for chat_id in kwargs["chat_ids"]],
        )
