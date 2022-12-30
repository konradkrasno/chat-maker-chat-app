from commons.settings import CommonSettings


class ApiSettings(CommonSettings):
    cookie_expiration_time_in_minutes: int = 5
    encryption_secret_key: str


def get_api_settings() -> ApiSettings:
    return ApiSettings()
