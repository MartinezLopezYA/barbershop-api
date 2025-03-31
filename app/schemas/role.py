from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .permission import Permission
else:
    Permission = None

class RoleBase(BaseModel):
    rolname: str = Field(..., example="Cajero")
    roldesc: Optional[str] = Field(..., example="Encargado de caja")
    rolstatus: bool = Field(..., example=True)

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleInDBBase(RoleBase):
    roluuid: UUID
    
    model_config = {"from_attributes": True}

class Role(RoleInDBBase):
    permissions: List["Permission"] = []
Role.model_rebuild()

class RoleSearchResults(BaseModel):
    count: int
    results: List[Role]