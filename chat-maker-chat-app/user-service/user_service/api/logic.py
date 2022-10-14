from fastapi import Depends
from fastapi.responses import JSONResponse
from user_service.api.models import SignInRequestModel
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
        return JSONResponse({"error": f"detail: {e.__str__()}"}, status_code=400)
    return JSONResponse({"user_id": new_user.id})
