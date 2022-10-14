from auth_service.api import logic
from fastapi import FastAPI


def endpoints(app: FastAPI):
    app.add_api_route(
        "/user/login",
        logic.login,
        methods=["POST"],
    )

    app.add_api_route(
        "/user/logout/{user_id}",
        logic.logout,
        methods=["GET"],
    )

    app.add_api_route(
        "/user/authenticate/{user_id}",
        logic.authenticate,
        methods=["POST"],
    )
