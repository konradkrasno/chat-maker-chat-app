from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from websocket_service.settings import get_ws_settings
from websocket_service.websocket.endpoints import endpoints as service_endpoints


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    service_endpoints(app)

    return app


if __name__ == "__main__":
    import uvicorn

    ws_settings = get_ws_settings()
    app = create_app()
    uvicorn.run(app, host=ws_settings.ws_service_url, port=ws_settings.ws_service_port)
