from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base, SessionLocal
from .routers import rooms, autocomplete
from . import crud, ws_manager
from sqlalchemy.orm import Session
import json

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Pair Programming - Prototype")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(autocomplete.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):
    await ws_manager.manager.connect(room_id, websocket)
    room = crud.get_room(db, room_id)
    if not room:
        await websocket.close(code=1000)
        return
    await websocket.send_json({"type": "init", "code": room.code})
    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            if data.get("type") == "code_update":
                code = data.get("code", "")
                crud.update_room_code(db, room_id, code)
                await ws_manager.manager.broadcast(room_id, {"type":"remote_update","code":code}, sender=websocket)
    except WebSocketDisconnect:
        await ws_manager.manager.disconnect(room_id, websocket)
