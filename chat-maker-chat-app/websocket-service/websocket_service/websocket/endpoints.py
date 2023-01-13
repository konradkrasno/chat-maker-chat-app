from fastapi import FastAPI
from websocket_service.websocket import logic


def endpoints(app: FastAPI):
    app.add_api_websocket_route(
        "/ws",
        logic.websocket_endpoint,
    )
