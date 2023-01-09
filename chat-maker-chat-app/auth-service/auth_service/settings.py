from commons.settings import CommonSettings


class ApiSettings(CommonSettings):
    encryption_secret_key: str
    cookie_expiration_time_in_minutes: int = 5
    origin_domain: str = "http://localhost:3000"


def get_api_settings() -> ApiSettings:
    return ApiSettings()
