from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

# Parent Blueprint for the database models
class Base(DeclarativeBase):
    pass


# Async Engine (Bridge)
engine = create_async_engine(settings.DATABASE_URL, echo=True)


# session factory (Assembly Line)

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    expire_on_commit=False
)


# Request Session Generator

async def get_db()->AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session