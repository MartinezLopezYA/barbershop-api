from pydantic import BaseModel
from uuid import UUID
from typing import List
from .role import Role

class PermissionBase(BaseModel):
    permissionname: str
    permissiondesc: str | None = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDBBase(PermissionBase):
    permissionuuid: UUID

    class Config:
        orm_mode = True

class Permission(PermissionInDBBase):
    roles: List[Role] = []

class PermissionSearchResults(BaseModel):
    count: int
    results: list[Permission]