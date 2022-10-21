from commons.api_models import BaseHeaders, BaseRequestModel


class AuthHeaders(BaseHeaders):
    authorization: str


class LoginRequestModel(BaseRequestModel):
    email: str
    password: str
