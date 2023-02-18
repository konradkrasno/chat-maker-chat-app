from typing import Dict

from chat_service.models import Message
from commons.clients import ChatServiceClient, get_chat_service_client
from fastapi import Depends, WebSocket


class ConnectionManager:
    def __init__(self, chat_service_client: ChatServiceClient):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_service_client = chat_service_client

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        del self.active_connections[user_id]

    async def broadcast(self, message: str, websocket: WebSocket = None):
        for connection in self.active_connections.values():
            if connection != websocket:
                await connection.send_text(message)

    async def send_message_to_chat(self, message: Message, chat_id: str):
        user_ids = await self.chat_service_client.get_chat_members(chat_id)
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


def get_connection_manager(
    chat_service_client: ChatServiceClient = Depends(get_chat_service_client),
) -> ConnectionManager:
    return ConnectionManager(chat_service_client=chat_service_client)
