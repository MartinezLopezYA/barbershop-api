from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import DateTime
from sqlalchemy.sql import func, text
from typing import List
from app.models import User as UserModel
from app.schemas import User, UserUpdate
from app.utils import security

async def create_user(db: AsyncSession, user_in: User) -> User:
    print(f"Creating user... {user_in}")
    
    if not user_in.username or not user_in.useremail or not user_in.userfirstname or not user_in.userlastname or not user_in.userpass:
        raise ValueError("Required values: username, useremail, firstname, lastname, password")
    
    # Verificar si el email ya está registrado
    db_user = await get_user_by_email(db, email=user_in.useremail)
    if db_user:
        raise ValueError("Email already registered")
    
    # Verificar si el username ya está tomado
    db_user = await get_user_by_username(db, username=user_in.username)
    if db_user:
        raise ValueError("Username already taken")
    
    # Hashear la contraseña
    hashed_password = security.generate_password_hash(user_in.userpass)
    
    # Crear el usuario
    db_user = UserModel(
        username=user_in.username,
        useremail=user_in.useremail,
        userfirstname=user_in.userfirstname,
        userlastname=user_in.userlastname,
        userphone=user_in.userphone,
        userstatus=user_in.userstatus,
        userpass=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Asignar roles al usuario en la tabla intermedia user_roles
    if hasattr(user_in, 'roles') and user_in.roles:
        for role_id in user_in.roles:
            await db.execute(
                text("INSERT INTO user_roles (useruuid, roluuid) VALUES (:useruuid, :roluuid)"),
                {"useruuid": db_user.useruuid, "roluuid": role_id}
            )
        await db.commit()
    
    # Retornar el usuario con los roles cargados
    result = await db.execute(
        select(UserModel).where(UserModel.useruuid == db_user.useruuid).options(selectinload(UserModel.roles))
    )
    db_user = result.scalar_one()
        # Convertir el modelo a un diccionario
    user_dict = {
        "useruuid": db_user.useruuid,
        "username": db_user.username,
        "useremail": db_user.useremail,
        "userfirstname": db_user.userfirstname,
        "userlastname": db_user.userlastname,
        "userphone": db_user.userphone,
        "userstatus": db_user.userstatus,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at,
        "roles": [role.roluuid for role in db_user.roles] if db_user.roles else None
    }
    
    return user_dict


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

async def get_user_by_email(db: AsyncSession, email: str) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.useremail == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.username == username))
    return result.scalar_one_or_none()