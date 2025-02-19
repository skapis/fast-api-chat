from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict] = []

    def get_active_connections(self, chat_id: str):
        return [conn for conn in self.active_connections if conn["chat_id"] == chat_id]

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()
        self.active_connections.append({"chat_id": chat_id, "websocket": websocket})

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [
            conn for conn in self.active_connections if conn["websocket"] != websocket
        ]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, chat_id: str):
        for connection in self.active_connections:
            if connection["chat_id"] == chat_id:
                await connection["websocket"].send_text(message)

manager = ConnectionManager()