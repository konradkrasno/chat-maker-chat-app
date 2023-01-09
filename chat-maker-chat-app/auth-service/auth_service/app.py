from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth_service.api.endpoints import endpoints as service_endpoints
from auth_service.settings import ApiSettings, get_api_settings


def create_app(settings: ApiSettings) -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    service_endpoints(app)

    return app


if __name__ == "__main__":
    import uvicorn

    api_settings = get_api_settings()
    app = create_app(api_settings)
    uvicorn.run(
        app, host=api_settings.auth_service_url, port=api_settings.auth_service_port
    )
