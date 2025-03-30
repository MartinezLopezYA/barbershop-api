from pydantic import BaseModel
from uuid import UUID

class UserRoleCreate(BaseModel):
    roluuid: UUID

class UserRole(BaseModel):
    useruuid: UUID
    roluuid: UUID

    class Config:
        orm_mode = True 