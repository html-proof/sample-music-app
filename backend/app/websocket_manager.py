from fastapi import WebSocket
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections: uid -> list of WebSockets (multi-device support)
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, uid: str):
        await websocket.accept()
        if uid not in self.active_connections:
            self.active_connections[uid] = []
        self.active_connections[uid].append(websocket)
        logger.info(f"User {uid} connected. Active devices: {len(self.active_connections[uid])}")

    def disconnect(self, websocket: WebSocket, uid: str):
        if uid in self.active_connections:
            if websocket in self.active_connections[uid]:
                self.active_connections[uid].remove(websocket)
            if not self.active_connections[uid]:
                del self.active_connections[uid]
        logger.info(f"User {uid} disconnected.")

    async def send_personal_message(self, message: dict, uid: str):
        if uid in self.active_connections:
            for connection in self.active_connections[uid]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to {uid}: {e}")

    async def broadcast(self, message: dict):
        for uid, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting: {e}")

manager = ConnectionManager()
