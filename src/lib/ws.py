from typing import Any

from fastapi import Depends
from fastapi import WebSocket as FastAPIWebSocket

from src.lib.session import Session, ws_session

connected_ws: dict[str, "WebSocket"] = {}


class WebSocket:
    ws: FastAPIWebSocket
    id: str
    session: Session

    @staticmethod
    async def connect(
        ws: FastAPIWebSocket, session: Session = Depends(ws_session)
    ) -> "WebSocket":
        await ws.accept()
        if not session.get("logged_in") or not session.get("user_id"):
            await ws.send_json({"type": "error", "message": "Unauthorized"})
            await ws.close(1000)
        socket = WebSocket()
        socket.ws = ws
        socket.session = session
        socket.id = session.get("user_id")
        if connected_ws.get(socket.id):
            await connected_ws[socket.id].disconnect()
        connected_ws[socket.id] = socket
        return socket

    @staticmethod
    def connections():
        return connected_ws

    async def disconnect(self):
        connected_ws.pop(self.id)
        await self.broadcast_json({"type": "disconnect", "id": self.id})
        await self.ws.close()

    async def broadcast(self, message: str):
        for uid, socket in connected_ws.items():
            if uid == self.id:
                continue
            await socket.ws.send_text(message)

    async def broadcast_json(self, json: Any):
        for uid, socket in connected_ws.items():
            if uid == self.id:
                continue
            await socket.ws.send_json(json)
