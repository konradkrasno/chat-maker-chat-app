from auth_service.dao import AuthDao, get_auth_dao
from auth_service.security import Cipher
from auth_service.settings import ApiSettings, get_api_settings
from fastapi import Cookie, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse


async def ping():
    return "pong"


async def login(
    device_id: str = Cookie(),
    email: str = Form(),
    password: str = Form(),
    auth_dao: AuthDao = Depends(get_auth_dao),
    settings: ApiSettings = Depends(get_api_settings),
):
    session = await auth_dao.create_session(email, password, device_id)
    if session:
        access_token = session.generate_token()
        response = RedirectResponse(
            settings.origin_domain, status_code=status.HTTP_302_FOUND
        )
        response.set_cookie(
            key="access_token",
            value=Cipher(secret_key=settings.encryption_secret_key).encrypt(
                access_token
            ),
            expires=settings.cookie_expiration_time_in_minutes * 60,
            httponly=True,
            secure=True,
            samesite="strict",
        )
        response.set_cookie(
            key="user_id",
            value=session.user_id,
        )
        return response
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
    )


async def logout(
    device_id: str = Cookie(),
    access_token: str = Cookie(),
    user_id: str = Cookie(),
    auth_dao: AuthDao = Depends(get_auth_dao),
    settings: ApiSettings = Depends(get_api_settings),
):
    auth_dao.logout(
        token=Cipher(secret_key=settings.encryption_secret_key).decrypt(access_token),
        user_id=user_id,
        device_id=device_id,
    )
    response = RedirectResponse(
        settings.origin_domain, status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie("access_token")
    response.delete_cookie("user_id")
    return response


async def authenticate(
    device_id: str = Cookie(),
    access_token: str = Cookie(),
    user_id: str = Cookie(),
    auth_dao: AuthDao = Depends(get_auth_dao),
    settings: ApiSettings = Depends(get_api_settings),
):
    try:
        token = Cipher(secret_key=settings.encryption_secret_key).decrypt(access_token)
    except (AssertionError, ValueError):
        pass
    else:
        if auth_dao.authenticate(
            token=token,
            user_id=user_id,
            device_id=device_id,
        ):
            return JSONResponse(
                {"ok": "User successfully authenticated"},
                status_code=status.HTTP_200_OK,
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired"
    )
