from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..db import SessionLocal

router = APIRouter(prefix="/rooms", tags=["rooms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.RoomOut)
def create_room(payload: schemas.RoomCreate, db: Session = Depends(get_db)):
    r = crud.create_room(db, language=payload.language)
    return {"roomId": r.id}
