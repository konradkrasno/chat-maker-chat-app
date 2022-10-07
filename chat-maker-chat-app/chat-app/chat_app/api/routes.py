from chat_app.api import logic
from fastapi import FastAPI


def endpoints(app: FastAPI):
    app.add_api_route(
        "/",
        logic.root,
        methods=["GET"],
    )

    app.add_api_route(
        "/chats/{user_id}",
        logic.get_user_chats,
        methods=["GET"],
    )

    app.add_api_route(
        "/chats/{user_id}/{chat_id}",
        logic.get_user_chat,
        methods=["GET"],
    )

    app.add_api_route(
        "/members/{user_id}",
        logic.get_chats_members_info,
        methods=["GET"],
    )