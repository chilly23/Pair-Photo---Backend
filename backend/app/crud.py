from sqlalchemy.orm import Session
from . import models
from uuid import uuid4

def create_room(db: Session, language: str = "python"):
    rid = str(uuid4())[:8]
    room = models.Room(id=rid, code="", language=language)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_room(db: Session, room_id: str):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def update_room_code(db: Session, room_id: str, code: str):
    r = get_room(db, room_id)
    if not r:
        return None
    r.code = code
    db.add(r)
    db.commit()
    db.refresh(r)
    return r
