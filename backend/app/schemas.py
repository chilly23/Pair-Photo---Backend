from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    language: Optional[str] = "python"

class RoomOut(BaseModel):
    roomId: str

class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

class AutocompleteResponse(BaseModel):
    suggestion: str
    cursor: int
