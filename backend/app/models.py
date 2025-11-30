from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from .db import Base

class Room(Base):
    __tablename__ = "rooms"
    id = Column(String, primary_key=True, index=True)
    code = Column(Text, default="")
    language = Column(String, default="python")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
