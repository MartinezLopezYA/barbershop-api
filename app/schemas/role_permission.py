from pydantic import BaseModel
from uuid import UUID

class RolePermissionCreate(BaseModel):
    permissionuuid: UUID

class RolePermission(BaseModel):
    roluuid: UUID
    permissionuuid: UUID

    class Config: 
        orm_mode = True