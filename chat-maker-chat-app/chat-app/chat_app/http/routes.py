from fastapi.responses import JSONResponse

from chat_app import app, dao
from chat_app.exceptions import ChatDoesNotExistsError


@app.get("/chats/{user_id}/{chat_id}")
async def get(user_id: str, chat_id: str):
    try:
        chats = dao.get_user_chat(user_id, chat_id)
    except ChatDoesNotExistsError as e:
        return JSONResponse({"error": e})
    return JSONResponse(chats)
