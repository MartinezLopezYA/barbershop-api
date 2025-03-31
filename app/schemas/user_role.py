from pydantic import BaseModel
from uuid import UUID

class UserRoleCreate(BaseModel):
    roluuid: UUID

class UserRole(BaseModel):
    useruuid: UUID
    roluuid: UUID

    model_config = {"from_attributes": True}