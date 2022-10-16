from chat_service.dao import ChatDao, get_chat_dao
from commons.exceptions import ItemDoesNotExistsError
from fastapi import Depends, status
from fastapi.responses import HTMLResponse, JSONResponse


async def root():
    return HTMLResponse("Hello World")


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
        return JSONResponse({"error": str(e)}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(chat.dict())


async def get_chats_members_info(
    user_id: str, dao: ChatDao = Depends(get_chat_dao)
) -> JSONResponse:
    try:
        members_info = dao.get_chats_members_info(user_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(members_info)
