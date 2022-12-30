from commons.api_models import BaseRequestModel


class LoginRequestModel(BaseRequestModel):
    email: str
    password: str
