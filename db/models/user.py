from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None # En mongo db el id es str
    username: str
    email: str