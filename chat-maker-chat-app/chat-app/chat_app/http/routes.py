from fastapi.responses import JSONResponse, HTMLResponse

from chat_app import app, dao
from chat_app.exceptions import ChatDoesNotExistsError


@app.get("/")
async def get():
    return HTMLResponse("Hello World")


@app.get("/chats/{user_id}")
async def get_user_chats(user_id: str):
    try:
        chats = dao.get_user_chats(user_id)
    except ChatDoesNotExistsError as e:
        return JSONResponse({"error": e})
    return JSONResponse({chat.id: chat.dict() for chat in chats})


@app.get("/chats/{user_id}/{chat_id}")
async def get_user_chat(user_id: str, chat_id: str):
    try:
        chat = dao.get_user_chat(user_id, chat_id)
    except ChatDoesNotExistsError as e:
        return JSONResponse({"error": e})
    return JSONResponse(chat.dict())
