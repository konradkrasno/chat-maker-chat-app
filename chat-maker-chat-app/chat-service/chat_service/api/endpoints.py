from chat_service.api import logic
from chat_service.api.models import (
    GetChatByUsersResponseModel,
    GetChatMembersResponseModel,
    GetChatsMembersInfoResponseModel,
    GetUserChatResponseModel,
    GetUserChatsResponseModel,
)
from commons.dependencies import verify_token
from fastapi import Depends, FastAPI


def endpoints(app: FastAPI):
    app.add_api_route(
        "/ping",
        logic.ping,
        methods=["GET"],
    )

    app.add_api_route(
        "/chats",
        logic.get_user_chats,
        methods=["GET"],
        dependencies=[Depends(verify_token)],
        response_model=GetUserChatsResponseModel,
    )

    app.add_api_route(
        "/chats/{chat_id}",
        logic.get_user_chat,
        methods=["GET"],
        dependencies=[Depends(verify_token)],
        response_model=GetUserChatResponseModel,
    )

    app.add_api_route(
        "/chats",
        logic.get_chat_by_users,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
        response_model=GetChatByUsersResponseModel,
    )

    app.add_api_route(
        "/members",
        logic.get_chat_members,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
        response_model=GetChatMembersResponseModel,
    )

    app.add_api_route(
        "/members",
        logic.get_chats_members_info,
        methods=["GET"],
        dependencies=[Depends(verify_token)],
        response_model=GetChatsMembersInfoResponseModel,
    )

    app.add_api_route(
        "/put-message",
        logic.put_message,
        methods=["POST"],
        dependencies=[Depends(verify_token)],
    )
