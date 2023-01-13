from chat_service.api.models import (
    GetChatByUsersRequestModel,
    GetChatByUsersResponseModel,
    GetChatsMembersInfoResponseModel,
    GetUserChatResponseModel,
    GetUserChatsResponseModel,
)
from chat_service.dao import ChatDao, get_chat_dao
from commons.exceptions import ItemDoesNotExistsError
from fastapi import Depends, HTTPException, status


async def ping():
    return "pong"


async def get_user_chats(
    dao: ChatDao = Depends(get_chat_dao),
) -> GetUserChatsResponseModel:
    chats = dao.get_user_chats()
    return GetUserChatsResponseModel(chats=chats)


async def get_user_chat(
    chat_id: str, dao: ChatDao = Depends(get_chat_dao)
) -> GetUserChatResponseModel:
    try:
        chat = dao.get_user_chat(chat_id)
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return GetUserChatResponseModel(chat=chat)


async def get_chat_by_users(
    data: GetChatByUsersRequestModel, dao: ChatDao = Depends(get_chat_dao)
) -> GetChatByUsersResponseModel:
    return GetChatByUsersResponseModel(
        chat=dao.get_chat_by_user(member_ids=data.user_ids)
    )


async def get_chats_members_info(
    dao: ChatDao = Depends(get_chat_dao),
) -> GetChatsMembersInfoResponseModel:
    try:
        members_info = await dao.get_chats_members_info()
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return GetChatsMembersInfoResponseModel(chats_members_info=members_info)


async def put_message(data, dao: ChatDao = Depends(get_chat_dao)):
    pass
