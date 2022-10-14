from commons.settings import CommonSettings


class ApiSettings(CommonSettings):
    pass


def get_api_settings() -> ApiSettings:
    return ApiSettings()
