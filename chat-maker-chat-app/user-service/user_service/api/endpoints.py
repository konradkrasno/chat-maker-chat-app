import socket

from commons.dependencies import constrain_access, verify_token
from fastapi import Depends, FastAPI
from user_service.api import logic
from user_service.settings import ApiSettings


def endpoints(app: FastAPI, settings: ApiSettings):
    app.add_api_route(
        "/user/sign-in",
        logic.sign_in,
        methods=["POST"],
    )

    app.add_api_route(
        "/user/query/{user_id}",
        logic.get_users_by_ids,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
    )

    app.add_api_route(
        "/user/creds",
        logic.get_user_creds,
        methods=["POST"],
        dependencies=[
            Depends(
                constrain_access(
                    allowed_hosts=[
                        socket.gethostbyname(settings.AUTH_SERVICE_URL),
                        socket.gethostbyname(settings.CHAT_SERVICE_URL),
                    ]
                )
            )
        ],
    )
