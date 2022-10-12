from chat_app.api.models import SignInRequestModel
from chat_app.dao import UserDao, get_user_dao
from fastapi import Depends
from fastapi.responses import HTMLResponse, JSONResponse


async def login():
    return HTMLResponse("Login endpoint")


async def logout():
    return HTMLResponse("Logout endpoint")


async def sign_in(
    request: SignInRequestModel = Depends(SignInRequestModel.load_from_request),
    user_dao: UserDao = Depends(get_user_dao),
):
    try:
        new_user = user_dao.create_user(
            name=request.name,
            surname=request.surname,
            email=request.email,
            password=request.password,
            avatar_source=request.avatar_source,
        )
    except Exception as e:
        return JSONResponse({"error": f"detail: {e.__str__()}"}, status_code=400)
    return JSONResponse({"user_id": new_user.id})
