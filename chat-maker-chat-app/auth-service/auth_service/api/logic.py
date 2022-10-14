from auth_service.api.models import AuthenticationHeaders, LoginRequestModel
from auth_service.dao import AuthDao, get_auth_dao
from fastapi import Depends, status
from fastapi.responses import JSONResponse

from commons.api_models import BaseHeaders


async def login(
    headers: BaseHeaders = Depends(BaseHeaders.get_headers),
    request: LoginRequestModel = Depends(LoginRequestModel.load_from_request),
    auth_dao: AuthDao = Depends(get_auth_dao),
):
    access_token = auth_dao.login(request.email, request.password, headers.device_id)
    if access_token:
        return JSONResponse({"access_token": access_token})
    return JSONResponse(
        {"error": "detail: Invalid email or password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def logout(
    user_id: str,
    headers: BaseHeaders = Depends(BaseHeaders.get_headers),
    auth_dao: AuthDao = Depends(get_auth_dao),
):
    auth_dao.logout(user_id, headers.device_id)
    return JSONResponse({"ok": "User logged out"})


async def authenticate(
    user_id: str,
    headers: AuthenticationHeaders = Depends(AuthenticationHeaders.get_headers),
    auth_dao: AuthDao = Depends(get_auth_dao),
):
    if auth_dao.authenticate(
        token=headers.authorization.replace("Bearer ", ""),
        user_id=user_id,
        device_id=headers.device_id,
    ):
        return JSONResponse({"ok": "User successfully authenticated"})
    return JSONResponse(
        {"error": "detail: Token invalid or expired"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
