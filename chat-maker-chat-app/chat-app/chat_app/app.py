from chat_app.api.routes import endpoints as api_endpoints
from chat_app.settings import ApiSettings, get_api_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app(settings: ApiSettings):
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_endpoints(app)

    return app


if __name__ == "__main__":
    import uvicorn

    api_settings = get_api_settings()
    app = create_app(api_settings)
    uvicorn.run(app, host="0.0.0.0", port=8000)
