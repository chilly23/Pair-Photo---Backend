from pydantic import BaseModel
from typing import Optional

class roomcreate(BaseModel):
    language: Optional[str] = "python"

class roomout(BaseModel):
    roomId: str

class autocomprequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

class autocompresponse(BaseModel):
    suggestion: str
    cursor: int
