from auth_service.api.models import LoginRequestModel
from auth_service.dao import AuthDao, get_auth_dao
from auth_service.security import Cipher
from auth_service.settings import ApiSettings, get_api_settings
from fastapi import Cookie, Depends, Header, status
from fastapi.responses import JSONResponse


async def login(
    device_id: str = Header(),
    request: LoginRequestModel = Depends(LoginRequestModel.load_from_request),
    auth_dao: AuthDao = Depends(get_auth_dao),
    settings: ApiSettings = Depends(get_api_settings),
):
    session = await auth_dao.create_session(request.email, request.password, device_id)
    if session:
        access_token = session.generate_token()
        response = JSONResponse(
            {"ok": "User logged in"}, status_code=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token",
            value=Cipher(secret_key=settings.encryption_secret_key).encrypt(
                access_token
            ),
            expires=settings.cookie_expiration_time_in_minutes * 60,
        )
        return response
    return JSONResponse(
        {"error": "detail: Invalid email or password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def logout(
    user_id: str,
    device_id: str = Header(),
    access_token: str = Cookie(),
    auth_dao: AuthDao = Depends(get_auth_dao),
    settings: ApiSettings = Depends(get_api_settings),
):
    auth_dao.logout(
        token=Cipher(secret_key=settings.encryption_secret_key).decrypt(access_token),
        user_id=user_id,
        device_id=device_id,
    )
    return JSONResponse({"ok": "User logged out"}, status_code=status.HTTP_200_OK)


async def authenticate(
    user_id: str,
    device_id: str = Header(),
    access_token: str = Cookie(),
    auth_dao: AuthDao = Depends(get_auth_dao),
    settings: ApiSettings = Depends(get_api_settings),
):
    if auth_dao.authenticate(
        token=Cipher(secret_key=settings.encryption_secret_key).decrypt(access_token),
        user_id=user_id,
        device_id=device_id,
    ):
        return JSONResponse(
            {"ok": "User successfully authenticated"}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        {"error": "detail: Token invalid or expired"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
