from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 declarative models."""
    pass


# Create async database engine
engine = create_async_engine(
    settings.async_database_url,
    echo=(settings.ENVIRONMENT == "development"),
    future=True,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async database session per request,
    ensuring proper cleanup and rollback on unhandled exceptions.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
