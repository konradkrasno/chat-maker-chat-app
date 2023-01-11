from typing import Dict, List

from chat_service.models import Chat
from pydantic import BaseModel
from user_service.models import User


class GetUserChatsResponseModel(BaseModel):
    chats: List[Chat]


class GetUserChatResponseModel(BaseModel):
    chat: Chat


class GetChatByUsersRequestModel(BaseModel):
    user_ids: List[str]


class GetChatByUsersResponseModel(BaseModel):
    chat: Chat


class GetChatsMembersInfoResponseModel(BaseModel):
    chats_members_info: Dict[str, List[User]]
