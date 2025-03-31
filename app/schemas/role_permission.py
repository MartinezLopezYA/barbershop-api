from pydantic import BaseModel
from uuid import UUID

class RolePermissionCreate(BaseModel):
    permissionuuid: UUID

class RolePermission(BaseModel):
    roluuid: UUID
    permissionuuid: UUID

    model_config = {"from_attributes": True}