from chat_service.dao import ChatDao, get_chat_dao
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse

from commons.exceptions import ItemDoesNotExistsError


async def ping():
    return "pong"


async def get_user_chats(
    user_id: str, dao: ChatDao = Depends(get_chat_dao)
) -> JSONResponse:
    chats = dao.get_user_chats(user_id)
    return JSONResponse({chat.id: chat.dict() for chat in chats})


async def get_user_chat(
    user_id: str, chat_id: str, dao: ChatDao = Depends(get_chat_dao)
) -> JSONResponse:
    try:
        chat = dao.get_user_chat(user_id, chat_id)
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())
    return JSONResponse(chat.dict())


async def get_chats_members_info(
    user_id: str, dao: ChatDao = Depends(get_chat_dao)
) -> JSONResponse:
    try:
        members_info = await dao.get_chats_members_info(user_id)
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())
    return JSONResponse(members_info)
