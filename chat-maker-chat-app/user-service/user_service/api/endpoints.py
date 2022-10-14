from fastapi import FastAPI
from user_service.api import logic


def endpoints(app: FastAPI):
    app.add_api_route(
        "/user/sign-in",
        logic.sign_in,
        methods=["POST"],
    )
