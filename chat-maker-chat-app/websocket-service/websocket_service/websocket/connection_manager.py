from typing import Dict

from chat_service.models import Message
from commons.clients import ChatServiceClient
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections.keys():
            del self.active_connections[user_id]

    async def broadcast(self, message: str, websocket: WebSocket = None):
        for connection in self.active_connections.values():
            if connection != websocket:
                await connection.send_text(message)

    async def send_message_to_chat(
        self, message: Message, chat_id: str, chat_service_client: ChatServiceClient
    ):
        user_ids = await chat_service_client.get_chat_members(chat_id)
        for user_id in user_ids:
            try:
                connection = self.active_connections[user_id]
            except KeyError:
                print(f"User #{user_id} is inactive")
            else:
                await connection.send_json(
                    {
                        "message": message.dict(),
                        "chatId": chat_id,
                    }
                )
