from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncSession: # type: ignore
    async with async_session_maker() as session:
        yield session