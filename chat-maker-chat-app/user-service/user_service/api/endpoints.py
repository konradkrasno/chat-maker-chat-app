from commons.dependencies import verify_token
from fastapi import Depends, FastAPI
from user_service.api import logic


def endpoints(app: FastAPI):
    app.add_api_route(
        "/user/sign-in",
        logic.sign_in,
        methods=["POST"],
    )

    app.add_api_route(
        "/user/query/{user_id}",
        logic.get_users_by_ids,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
    )
