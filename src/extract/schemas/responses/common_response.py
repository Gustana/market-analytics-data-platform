from pydantic import BaseModel

class Paggination(BaseModel):
    limit: int
    offset: int
    count: int
    total: int

class FixerErrorRecord(BaseModel):
    code: int
    info: str