from commons.clients import AuthServiceClient, get_auth_service_client
from fastapi import Depends, HTTPException


async def verify_token(
    user_id: str,
    auth_service_client: AuthServiceClient = Depends(get_auth_service_client),
):
    if not auth_service_client.authenticate(user_id=user_id):
        raise HTTPException(status_code=401, detail="Unauthorized token.")
