from pydantic import BaseModel
from uuid import UUID
from typing import List
from .permission import Permission

class RoleBase(BaseModel):
    rolname: str
    roldesc: str | None = None
    rolstatus: bool = True

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleInDBBase(RoleBase):
    roluuid: UUID
    
    class Config:
        orm_mode = True

class Role(RoleInDBBase):
    permissions: List[Permission] = []

class RoleSearchResults(BaseModel):
    count: int
    results: list[Role]