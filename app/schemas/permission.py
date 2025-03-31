from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .role import Role

class PermissionBase(BaseModel):
    permissionname: str
    permissiondesc: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDBBase(PermissionBase):
    permissionuuid: UUID

    model_config = {"from_attributes": True}

class Permission(PermissionInDBBase):
    roles: List["Role"] = []

class PermissionSearchResults(BaseModel):
    count: int
    results: List[Permission]