from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List
from .role import Role

class UserBase(BaseModel):
    username: str
    useremail: str
    userfirstname: str
    userlastname: str
    userphone: str | None
    userstatus: bool = True

class UserCreate(UserBase):
    userpass: str

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    useruuid: UUID
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
    
class User(UserInDBBase):
    roles: List[Role] = []

class UserSearchResults(BaseModel):
    count: int
    results: list[User]