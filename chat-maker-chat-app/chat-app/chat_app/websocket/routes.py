from fastapi import WebSocket, WebSocketDisconnect

from app import app
from app.websocket import manager


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{user_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            # await manager.send_personal_message(f"You wrote: {data.get('content')}", websocket)
            await manager.broadcast(
                f"Client #{user_id} says: {data.get('content')}", websocket
            )
            # put_message(chats, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
