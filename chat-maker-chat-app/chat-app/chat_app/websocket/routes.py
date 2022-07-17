from fastapi import WebSocket, WebSocketDisconnect

from chat_app import app
from chat_app.websocket import manager
from chat_app import dao


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
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
