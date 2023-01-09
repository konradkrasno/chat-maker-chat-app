from commons.exceptions import ItemDoesNotExistsError
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from user_service.api.models import (
    GetUserCredsRequestModel,
    GetUsersByIdsRequestModel,
    SignInRequestModel,
)
from user_service.dao import UserDao, get_user_dao


async def sign_in(
    data: SignInRequestModel,
    user_dao: UserDao = Depends(get_user_dao),
):
    try:
        new_user = user_dao.create_user(
            name=data.name,
            surname=data.surname,
            email=data.email,
            password=data.password,
            avatar_source=data.avatar_source,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse({"user_id": new_user.id})


async def get_users_by_ids(
    data: GetUsersByIdsRequestModel,
    user_dao: UserDao = Depends(get_user_dao),
):
    try:
        return JSONResponse(user_dao.get_users_by_ids(data.user_ids))
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def get_user_by_id(
    user_id: str,
    user_dao: UserDao = Depends(get_user_dao),
):
    try:
        return user_dao.get_users_by_ids([user_id])[0]
    except ItemDoesNotExistsError:
        return JSONResponse({})


async def get_user_creds(
    data: GetUserCredsRequestModel,
    user_dao: UserDao = Depends(get_user_dao),
):
    try:
        return JSONResponse(user_dao.get_user_creds(data.email))
    except ItemDoesNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
