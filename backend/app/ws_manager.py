from typing import Dict, List
from fastapi import WebSocket
import asyncio

class connectionmanager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active.setdefault(room, []).append(websocket)

    async def disconnect(self, room: str, websocket: WebSocket):
        async with self._lock:
            conns = self.active.get(room, [])
            if websocket in conns:
                conns.remove(websocket)
            if not conns:
                self.active.pop(room, None)

    async def broadcast(self, room: str, message: dict, sender: WebSocket = None):
        async with self._lock:
            conns = list(self.active.get(room, []))
        for ws in conns:
            if ws is sender:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                # ignore send errors but clean up later
                pass

manager = ConnectionManager()
