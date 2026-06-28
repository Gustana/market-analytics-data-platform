from pydantic import BaseModel

class PaginationRecords(BaseModel):
    limit: int
    offset: int
    count: int
    total: int

class ErrorRecords(BaseModel):
    code: int
    info: str