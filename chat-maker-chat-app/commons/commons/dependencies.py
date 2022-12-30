from typing import Callable, List

from fastapi import Depends, HTTPException, Request, status

from commons.clients import AuthServiceClient, get_auth_service_client


async def verify_token(
    user_id: str,
    auth_service_client: AuthServiceClient = Depends(get_auth_service_client),
) -> None:
    if not auth_service_client.authenticate(user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized token."
        )


def constrain_access(allowed_hosts: List[str]) -> Callable:
    def check_host(request: Request) -> None:
        ip = request.client.host
        if ip not in allowed_hosts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"IP {ip} is not allowed to access this resource.",
            )

    return check_host
