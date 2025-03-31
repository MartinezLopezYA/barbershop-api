from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role
else:
    Role = None

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    useremail: str = Field(..., example="johndoe@gmail.com")
    userfirstname: str = Field(..., example="John")
    userlastname: str = Field(..., example="Doe")
    userphone: Optional[str] = Field(..., example="3212346789")
    userstatus: bool = Field(..., example=True)

class UserCreate(UserBase):
    userpass: str

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    useruuid: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class User(UserInDBBase):
    roles: List["Role"] = []
User.model_rebuild()

class UserSearchResults(BaseModel):
    count: int
    results: List[User]