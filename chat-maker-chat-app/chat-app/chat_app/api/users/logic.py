from chat_app.dao import UserDao, get_user_dao
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse


async def login():
    return HTMLResponse("Login endpoint")


async def logout():
    return HTMLResponse("Logout endpoint")


async def sign_in(request: Request, user_dao: UserDao = Depends(get_user_dao)):
    # TODO finish

    return HTMLResponse("Sign in endpoint")
