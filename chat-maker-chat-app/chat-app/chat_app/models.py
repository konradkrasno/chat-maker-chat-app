import re
from hashlib import sha256
from typing import List
from uuid import uuid4

from pydantic import BaseModel, validator


class User(BaseModel):
    id: str
    avatarSource: str
    name: str
    surname: str

    @classmethod
    def create_item(cls, _id: str, avatar_source: str, name: str, surname: str):
        return cls.load_from_dict(
            id=_id, avatarSource=avatar_source, name=name, surname=surname
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)


class UserCreds(BaseModel):
    id: str
    email: str
    password: str
    salt: str

    @classmethod
    def create_item(cls, _id: str, email: str, password: str):
        salt = cls._get_salt()
        return cls.load_from_dict(
            id=_id,
            email=email,
            password=cls._hash_password(password, salt),
            salt=salt,
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)

    @validator("email")
    def check_email(cls, v):
        if not re.findall("^[\\w\\.\\-_]+@[\\w\\.\\-_]+\\.[\\w]+$", v):
            raise ValueError(f"Invalid email value: '{v}'")
        return v

    @validator("password")
    def check_password(cls, v):
        if len(v) < 7:
            raise ValueError("Password must have at least 8 chars")
        return v

    @staticmethod
    def _get_salt() -> str:
        return uuid4().hex[:6]

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        salted_password = f"{salt}{password}"
        return sha256(salted_password.encode()).hexdigest()

    def is_valid(self, password: str) -> bool:
        if self._hash_password(password, self.salt) == self.password:
            return True
        return False


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
