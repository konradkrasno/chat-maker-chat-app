from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user_service.api.endpoints import endpoints as service_endpoints
from user_service.settings import ApiSettings, get_api_settings


def create_app(settings: ApiSettings) -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
