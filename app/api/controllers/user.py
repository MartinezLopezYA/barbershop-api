from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from typing import List
from app.schemas import UserCreate, UserUpdate, User
from app.services import user

user_router = APIRouter()

@user_router.post("/create-user", response_model=User, description="Provide an endpoint to create a new user in database")
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user.create_user(db=db, user_in=user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_router.get("/get-users", response_model=List[User], description="Provide an endpoint to get all users in database")
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        return await user.get_users(db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.patch("/update-user/{useruuid}", response_model=User, description="Provide an endpoint to update an user from database according to its uuid")
async def patch_user(useruuid: str, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_user = await user.update_user(db=db, useruuid=useruuid, user_in=user_in)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_router.patch("/change-status-user/{useruuid}", response_model={}, description="Provide an endpoint to change status from an user")
async def change_status(useruuid: str, db: AsyncSession = Depends(get_db)):
    try: 
        changed_status = await user.change_status(db=db, useruuid=useruuid)
        if not changed_status:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "status": "OK",
            "message": "Status changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.delete("/delete-user/{useruuid}", response_model={}, description="Provide an endpoint to delete an user")
async def delete_user(useruuid: str, db: AsyncSession = Depends(get_db)):
    try:
        deleted_user = await user.delete_user(db=db, useruuid=useruuid)
        if not deleted_user:
            raise HTTPException(status_code=400, detail="Role not found")
        return {
            "status": "OK",
            "message": "Role deleted successfully",
            "deleted_user": str(deleted_user.username)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))