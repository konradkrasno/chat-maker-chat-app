from chat_app.dao import Dao, get_dao
from chat_app.exceptions import ItemDoesNotExistsError
from fastapi import Depends
from fastapi.responses import HTMLResponse, JSONResponse


async def root():
    return HTMLResponse("Hello World")


async def get_user_chats(user_id: str, dao: Dao = Depends(get_dao)) -> JSONResponse:
    try:
        chats = dao.get_user_chats(user_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)})
    return JSONResponse({chat.id: chat.dict() for chat in chats})


async def get_user_chat(
    user_id: str, chat_id: str, dao: Dao = Depends(get_dao)
) -> JSONResponse:
    try:
        chat = dao.get_user_chat(user_id, chat_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)})
    return JSONResponse(chat.dict())


async def get_chats_members_info(
    user_id: str, dao: Dao = Depends(get_dao)
) -> JSONResponse:
    try:
        members_info = dao.get_chats_members_info(user_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)})
    return JSONResponse(members_info)
