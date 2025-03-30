from sqlalchemy import inspect
from app.database.database import Base, engine

async def create_tables_if_not_exists():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas o ya existentes (async).")