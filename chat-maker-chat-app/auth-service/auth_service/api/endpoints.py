from auth_service.api import logic
from fastapi import FastAPI


def endpoints(app: FastAPI):
    app.add_api_route(
        "/ping",
        logic.ping,
        methods=["GET"],
    )

    app.add_api_route(
        "/auth/login",
        logic.login,
        methods=["POST"],
    )

    app.add_api_route(
        "/auth/logout",
        logic.logout,
        methods=["GET"],
    )

    app.add_api_route(
        "/auth/authenticate",
        logic.authenticate,
        methods=["POST"],
    )
