from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.models import Role
from app.schemas import RoleCreate, RoleUpdate
from typing import List

async def create_role(db:AsyncSession, role_in: RoleCreate) -> Role:
    if not role_in.rolname:
        raise ValueError("Required values: rolname")
    db_role = await get_role_by_name(db, rolname=role_in.rolname) 
    if db_role:
        raise ValueError("Rol already exists")
    db_role = Role(**role_in.model_dump())
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    result = await db.execute(select(Role).where(Role.roluuid == db_role.roluuid).options(selectinload(Role.permissions)))
    return result.scalar_one()

async def get_roles(db: AsyncSession) -> List[Role]:
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions))
    )
    return result.scalars().all()

async def update_rol(db: AsyncSession, roluuid: str, role_in: RoleUpdate) -> Role | None:
    if not role_in.rolname:
        raise ValueError("Required values: rolname")
    result = await db.execute(select(Role).where(Role.roluuid == roluuid))
    db_role = result.scalar_one_or_none()

    if not db_role:
        return None

    if role_in.rolname != db_role.rolname:
        existing_role_by_name = await get_role_by_name(db, rolname=role_in.rolname)
        if existing_role_by_name and existing_role_by_name.roluuid != roluuid:
            raise ValueError("Rol's name already taken") 
    
    update_rol = role_in.model_dump(exclude_unset=True)
    for key, value in update_rol.items():
        setattr(db_role, key, value)

    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    refreshed_result = await db.execute(
        select(Role)
        .where(Role.roluuid == roluuid)
        .options(selectinload(Role.permissions))
    )
    return refreshed_result.scalar_one()

async def change_status(db: AsyncSession, roluuid: str) -> Role | None:
    result = await db.execute(select(Role).where(Role.roluuid == roluuid))
    db_role = result.scalar_one_or_none()

    if not db_role:
        return None
    
    db_role.rolstatus = not db_role.rolstatus

    await db.commit()
    await db.refresh(db_role)
    return db_role

async def delete_role(db: AsyncSession, roluuid: str) -> Role | None:
    result = await db.execute(select(Role).where(Role.roluuid == roluuid))
    db_role = result.scalar_one_or_none()

    if not db_role:
        return None
    
    await db.delete(db_role)
    await db.commit()
    return db_role

async def get_role_by_name(db: AsyncSession, rolname: str) -> Role | None:
    result = await db.execute(select(Role).filter(Role.rolname == rolname))
    return result.scalar_one_or_none()