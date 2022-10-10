from chat_app.api.users import logic
from fastapi import FastAPI


def endpoints(app: FastAPI):
    app.add_api_route(
        "/user/{user_id}/login",
        logic.login,
        methods=["POST"],
    )

    app.add_api_route(
        "/user/{user_id}/logout",
        logic.logout,
        methods=["GET"],
    )

    app.add_api_route(
        "/user/{user_id}/sign-in",
        logic.sign_in,
        methods=["POST"],
    )
