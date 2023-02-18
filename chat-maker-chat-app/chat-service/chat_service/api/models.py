from typing import Dict, List

from chat_service.models import Chat, Message
from pydantic import BaseModel
from user_service.models import User


class GetUserChatsResponseModel(BaseModel):
    chats: List[Chat]


class GetUserChatResponseModel(BaseModel):
    chat: Dict


class GetChatByUsersRequestModel(BaseModel):
    user_ids: List[str]


class GetChatByUsersResponseModel(BaseModel):
    chat: Chat


class GetChatMembersRequestModel(BaseModel):
    chat_id: str


class GetChatMembersResponseModel(BaseModel):
    members: List[str]


class GetChatsMembersInfoResponseModel(BaseModel):
    chats_members_info: Dict[str, List[User]]


class PutMessageRequestModel(BaseModel):
    chat_id: str
    message: Message
