from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from typing import List
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.utils import security

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    if not user_in.username or not user_in.useremail or not user_in.userfirstname or not user_in.userlastname or not user_in.userpass:
        raise ValueError("Required values: username, useremail, firstname, lastname, password")
    db_user = await get_user_by_email(db, email=user_in.useremail)
    if db_user:
        raise ValueError("Email already registered")
    db_user = await get_user_by_username(db, username=user_in.username)
    if db_user:
        raise ValueError("Username already taken")
    hashed_password = security.generate_password_hash(user_in.userpass)
    db_user = User(**user_in.model_dump(exclude={"userpass"}), userpass=hashed_password)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    result = await db.execute(select(User).where(User.useruuid == db_user.useruuid).options(selectinload(User.roles)))
    return result.scalar_one()

async def get_user(db: AsyncSession, useruuid: str) -> User | None:
    result = await db.execute(
        select(User)
        .filter(User.useruuid == useruuid)
        .options(selectinload(User.roles))
    )
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
    )
    return result.scalars().all()

async def update_user(db: AsyncSession, useruuid: str, user_in: UserUpdate) -> User | None:
    if not user_in.username or not user_in.useremail or not user_in.userfirstname or not user_in.userlastname or not user_in.userpass:
        raise ValueError("Required values: username, useremail, firstname, lastname, password")
    result = await db.execute(select(User).where(User.useruuid == useruuid))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None

    if user_in.useremail and user_in.useremail != db_user.useremail:
        existing_user_by_email = await get_user_by_email(db, email=user_in.useremail)
        if existing_user_by_email and existing_user_by_email.useruuid != useruuid:
            raise ValueError("Email already registered")

    if user_in.username and user_in.username != db_user.username:
        existing_user_by_username = await get_user_by_username(db, username=user_in.username)
        if existing_user_by_username and existing_user_by_username.useruuid != useruuid:
            raise ValueError("Username already taken")
        
    update_user = user_in.model_dump(exclude_unset=True)
    for key, value in update_user.items():
        setattr(db_user, key, value)

    db_user.updated_at = func.now()

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    refreshed_result = await db.execute(
        select(User)
        .where(User.useruuid == useruuid)
        .options(selectinload(User.roles))
    )
    return refreshed_result.scalar_one()

async def change_status(db: AsyncSession, useruuid: str) -> User | None:
    result = await db.execute(select(User).where(User.useruuid == useruuid))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None
    
    db_user.userstatus = not db_user.userstatus
    db_user.updated_at = func.now()

    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, useruuid: str) -> User | None:
    result = await db.execute(select(User).where(User.useruuid == useruuid))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None
    
    await db.delete(db_user)
    await db.commit()
    return db_user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.useremail == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()