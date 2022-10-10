from typing import List

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
