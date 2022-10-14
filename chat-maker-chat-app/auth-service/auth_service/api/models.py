from commons.api_models import BaseHeaders, BaseRequestModel


class AuthenticationHeaders(BaseHeaders):
    authorization: str


class LoginRequestModel(BaseRequestModel):
    email: str
    password: str
