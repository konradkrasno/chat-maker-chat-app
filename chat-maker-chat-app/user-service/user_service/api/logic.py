from commons.exceptions import ItemDoesNotExistsError
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from user_service.api.models import (
    GetUserCredsRequestModel,
    GetUsersByIdsRequestModel,
    SignInRequestModel,
)
from user_service.dao import UserDao, get_user_dao


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
        return JSONResponse(
            {"error": f"detail: {e.__str__()}"}, status_code=status.HTTP_400_BAD_REQUEST
        )
    return JSONResponse({"user_id": new_user.id})


async def get_users_by_ids(
    request: GetUsersByIdsRequestModel = Depends(
        GetUsersByIdsRequestModel.load_from_request
    ),
    user_dao: UserDao = Depends(get_user_dao),
):
    return JSONResponse(user_dao.get_users_by_ids(request.user_ids))


async def get_user_creds(
    request: GetUserCredsRequestModel = Depends(
        GetUserCredsRequestModel.load_from_request
    ),
    user_dao: UserDao = Depends(get_user_dao),
):
    try:
        return JSONResponse(user_dao.get_user_creds(request.email))
    except ItemDoesNotExistsError as e:
        return JSONResponse(
            {"error": f"detail: {e.__str__()}"}, status_code=status.HTTP_404_NOT_FOUND
        )
