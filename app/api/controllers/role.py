from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from typing import List

from app.schemas import RoleCreate, Role, RoleUpdate
from app.services import role

role_router = APIRouter()

@role_router.post("/create-role", response_model=Role, description="Provide an endpoint to create a new role in database")
async def create_role(role_in: RoleCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await role.create_role(db=db, role_in=role_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@role_router.get("/get-roles", response_model=List[Role], description="Provide an endpoint to get all roles in database")
async def get_roles(db: AsyncSession = Depends(get_db)):
    try: 
        return await role.get_roles(db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@role_router.patch("/update-role/{roluuid}", response_model=Role, description="Provide an endpoint to update an role from database according to its uuid")
async def patch_user(roluuid: str, role_in: RoleUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_role = await role.update_rol(db=db, roluuid=roluuid, role_in=role_in)
        if not updated_role:
            raise HTTPException(status_code=404, detail="Role not found")
        return updated_role
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@role_router.patch("/change-status-role/{roluuid}", response_model={}, description="Provide an endpoint to change status from an role")
async def change_status(roluuid: str, db: AsyncSession = Depends(get_db)):
    try: 
        changed_status = await role.change_status(db=db, roluuid=roluuid)
        if not changed_status:
            raise HTTPException(status_code=404, detail="Role not found")
        return {
            "status": "OK",
            "message": "Status changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@role_router.delete("/delete-role/{roluuid}", response_model={}, description="Provide an endpoint to delete a role")
async def delete_role(roluuid: str, db: AsyncSession = Depends(get_db)):
    try:
        deleted_role = await role.delete_role(db=db, roluuid=roluuid)
        if not deleted_role:
            raise HTTPException(status_code=400, detail="Role not found")
        return {
            "status": "OK",
            "message": "Role deleted successfully",
            "deleted_role": str(deleted_role.rolname)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
