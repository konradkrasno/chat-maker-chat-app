from fastapi.responses import JSONResponse, HTMLResponse

from chat_app import app, dao
from chat_app.exceptions import ItemDoesNotExistsError


@app.get("/")
async def get():
    return HTMLResponse("Hello World")


@app.get("/chats/{user_id}")
async def get_user_chats(user_id: str) -> JSONResponse:
    try:
        chats = dao.get_user_chats(user_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)})
    return JSONResponse({chat.id: chat.dict() for chat in chats})


@app.get("/chats/{user_id}/{chat_id}")
async def get_user_chat(user_id: str, chat_id: str) -> JSONResponse:
    try:
        chat = dao.get_user_chat(user_id, chat_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)})
    return JSONResponse(chat.dict())


@app.get("/members/{user_id}")
async def get_chats_members_info(user_id: str) -> JSONResponse:
    try:
        members_info = dao.get_chats_members_info(user_id)
    except ItemDoesNotExistsError as e:
        return JSONResponse({"error": str(e)})
    return JSONResponse(members_info)
