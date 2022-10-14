from chat_service.dao import ChatDao, get_chat_dao
from fastapi import Depends, WebSocket, WebSocketDisconnect
from websocket_service.websocket.connection_manager import (
    ConnectionManager,
    get_connection_manager,
)


async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    dao: ChatDao = Depends(get_chat_dao),
    manager: ConnectionManager = Depends(get_connection_manager),
):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{user_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_json()
            chat_id = data.get("chatId")
            message = data.get("message")
            # await manager.send_personal_message(f"You wrote: {data.get('content')}", websocket)
            await manager.broadcast(
                f"Client #{user_id} says: {message.get('content')}", websocket
            )
            dao.put_message(user_id, chat_id, message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
