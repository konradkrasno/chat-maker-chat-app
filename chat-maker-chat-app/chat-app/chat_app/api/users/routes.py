from chat_app.api.users import logic
from fastapi import FastAPI


def endpoints(app: FastAPI):
    app.add_api_route(
        "/user/login/{user_id}",
        logic.login,
        methods=["POST"],
    )

    app.add_api_route(
        "/user/logout/{user_id}",
        logic.logout,
        methods=["GET"],
    )

    app.add_api_route(
        "/user/sign-in",
        logic.sign_in,
        methods=["POST"],
    )
