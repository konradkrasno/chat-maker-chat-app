import socket

from commons.dependencies import constrain_access, verify_token
from fastapi import Depends, FastAPI
from user_service.api import logic
from user_service.api.models import (
    GetUserByIdResponseModel,
    GetUserCredsResponseModel,
    GetUsersByIdsResponseModel,
    SearchUsersResponseModel,
    SignInResponseModel,
)
from user_service.settings import ApiSettings


def endpoints(app: FastAPI, settings: ApiSettings):
    app.add_api_route(
        "/user/sign-in",
        logic.sign_in,
        methods=["POST"],
        response_model=SignInResponseModel,
    )

    app.add_api_route(
        "/user/query",
        logic.get_users_by_ids,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
        response_model=GetUsersByIdsResponseModel,
    )

    app.add_api_route(
        "/user/id",
        logic.get_user_by_id,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
        response_model=GetUserByIdResponseModel,
    )

    app.add_api_route(
        "/user/creds",
        logic.get_user_creds,
        methods=["POST"],
        dependencies=[
            Depends(
                constrain_access(
                    allowed_hosts=[
                        socket.gethostbyname(settings.auth_service_url),
                        socket.gethostbyname(settings.chat_service_url),
                    ]
                )
            )
        ],
        response_model=GetUserCredsResponseModel,
    )

    app.add_api_route(
        "/user/search",
        logic.search_users,
        methods=["GET"],
        dependencies=[Depends(verify_token)],
        response_model=SearchUsersResponseModel,
    )
