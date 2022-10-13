from hashlib import sha256
from typing import Dict, List
from uuid import uuid4

import arrow
import jwt
from pydantic import BaseModel


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
    user_id: str
    email: str
    password: str
    salt: str

    @classmethod
    def create_item(cls, user_id: str, email: str, password: str):
        salt = cls._get_salt()
        return cls.load_from_dict(
            user_id=user_id,
            email=email,
            password=cls._hash_password(password, salt),
            salt=salt,
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)

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


class Session(BaseModel):
    id: str
    user_id: str
    device_id: str
    secret: str

    class TokenPayload(BaseModel):
        user_id: str
        time_to_expiry: int
        session_id: str
        device_id: str

        @classmethod
        def create_payload(cls, user_id: str, session_id: str, device_id: str) -> Dict:
            return cls(
                user_id=user_id,
                time_to_expiry=arrow.now().shift(hours=1).timestamp(),
                session_id=session_id,
                device_id=device_id,
            ).dict()

    def generate_token(self) -> str:
        token_payload = self.TokenPayload.create_payload(
            user_id=self.user_id, session_id=self.id, device_id=self.device_id
        )
        return jwt.encode(token_payload, self.secret, algorithm="HS256")

    @classmethod
    def create_item(cls, user_id: str, device_id: str):
        return cls(
            id=uuid4().hex,
            user_id=user_id,
            device_id=device_id,
            secret=uuid4().hex,
        )

    @classmethod
    def load_from_dict(cls, **kwargs):
        return cls(**kwargs)


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
