from fastapi import Depends, status
from fastapi.responses import HTMLResponse, JSONResponse

from chat_app.api.models import (
    AuthenticationHeaders,
    BaseHeaders,
    LoginRequestModel,
    SignInRequestModel,
)
from chat_app.dao import UserDao, get_user_dao


async def login(
    headers: BaseHeaders = Depends(BaseHeaders.get_headers),
    request: LoginRequestModel = Depends(LoginRequestModel.load_from_request),
    user_dao: UserDao = Depends(get_user_dao),
):
    access_token = user_dao.login(request.email, request.password, headers.device_id)
    if access_token:
        return JSONResponse({"access_token": access_token})
    return JSONResponse(
        {"error": "detail: Invalid email or password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def logout():
    # TODO finish
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


async def authenticate(
    user_id: str,
    headers: AuthenticationHeaders = Depends(AuthenticationHeaders.get_headers),
    user_dao: UserDao = Depends(get_user_dao),
):
    if user_dao.authenticate(
        token=headers.authorization.replace("Bearer ", ""),
        user_id=user_id,
        device_id=headers.device_id,
    ):
        return JSONResponse({"ok": "User successfully authenticated"})
    return JSONResponse(
        {"error": "detail: Token invalid or expired"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
