from chat_service.api.models import (
    GetChatByUsersRequestModel,
    GetChatByUsersResponseModel,
    GetChatMembersRequestModel,
    GetChatMembersResponseModel,
    GetChatsMembersInfoResponseModel,
    GetUserChatResponseModel,
    GetUserChatsResponseModel,
    PutMessageRequestModel,
)
from chat_service.dao import ChatDao, get_chat_dao
from commons.exceptions import ItemDoesNotExistsError
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse


async def ping():
    return "pong"


async def get_user_chats(
    dao: ChatDao = Depends(get_chat_dao),
) -> GetUserChatsResponseModel:
    chats = dao.get_user_chats()
    return GetUserChatsResponseModel(chats=chats)


async def get_user_chat(
    data: GetChatMembersRequestModel, dao: ChatDao = Depends(get_chat_dao)
) -> GetUserChatResponseModel:
    try:
        chat = await dao.get_user_chat_with_sender_data(data.chat_id)
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return GetUserChatResponseModel(chat=chat)


async def get_chat_by_users(
    data: GetChatByUsersRequestModel, dao: ChatDao = Depends(get_chat_dao)
) -> GetChatByUsersResponseModel:
    return GetChatByUsersResponseModel(
        chat=dao.get_chat_by_users(member_ids=data.user_ids)
    )


async def get_chat_members(
    data: GetChatMembersRequestModel, dao: ChatDao = Depends(get_chat_dao)
) -> GetChatMembersResponseModel:
    try:
        members = dao.get_chat_members(data.chat_id)
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return GetChatMembersResponseModel(members=members)


async def get_chats_members_info(
    dao: ChatDao = Depends(get_chat_dao),
) -> GetChatsMembersInfoResponseModel:
    try:
        members_info = await dao.get_chats_members_info()
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return GetChatsMembersInfoResponseModel(chats_members_info=members_info)


async def put_message(
    data: PutMessageRequestModel, dao: ChatDao = Depends(get_chat_dao)
):
    try:
        dao.put_message(data.chat_id, message=data.message)
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return JSONResponse({"status": "ok"})
