from chat_service.models import Message
from commons.clients import (
    AuthServiceClient,
    ChatServiceClient,
    get_auth_service_client,
    get_chat_service_client,
)
from fastapi import Cookie, Depends, WebSocket, WebSocketDisconnect, status
from websocket_service.websocket.connection_manager import (
    ConnectionManager,
    get_connection_manager,
)


async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str = Cookie(default=None),
    manager: ConnectionManager = Depends(get_connection_manager),
    auth_service_client: AuthServiceClient = Depends(get_auth_service_client),
    chat_service_client: ChatServiceClient = Depends(get_chat_service_client),
):
    if not auth_service_client.authenticate():
        raise WebSocketDisconnect(
            code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized token."
        )

    await manager.connect(websocket)
    await manager.broadcast(f"Client #{user_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_json()
            print("data:", data)
            chat_id = data["chat_id"]
            message_data = data["message"]
            message = Message.load_from_dict(**message_data)
            # await manager.send_personal_message(f"You wrote: {data.get('content')}", websocket)
            await manager.broadcast(
                f"Client #{user_id} says: {message.content}", websocket
            )
            await chat_service_client.put_message(chat_id, message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
