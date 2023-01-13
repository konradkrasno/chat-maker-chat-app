from commons.settings import CommonSettings


class WSSettings(CommonSettings):
    pass


def get_ws_settings() -> WSSettings:
    return WSSettings()
