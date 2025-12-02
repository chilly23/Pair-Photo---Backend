from fastapi import APIRouter
from ..schemas import autocomprequest, autocompresponse

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])

@router.post("", response_model=autocompresponse)
def autocomplete(req: autocomprequest):
    tail = req.code[:req.cursorPosition].split()[-1] if req.cursorPosition > 0 and req.code.strip() else ""
    if tail.endswith("import"):
        suggestion = " os\n"
    elif tail == "def":
        suggestion = " func_name():\n    pass\n"
    elif tail.endswith("print"):
        suggestion = "(\"hello\")"
    else:
        suggestion = "def helper():\n    return None\n"
    return {"suggestion": suggestion, "cursor": req.cursorPosition + len(suggestion)}
