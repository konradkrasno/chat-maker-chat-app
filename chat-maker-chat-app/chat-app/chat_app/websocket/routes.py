from chat_app.websocket import logic
from fastapi import FastAPI


def endpoints(app: FastAPI):
    app.add_websocket_route(
        "/ws/{user_id}",
        logic.websocket_endpoint,
    )
