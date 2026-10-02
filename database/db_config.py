from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base , sessionmaker
from config.settings import settings


DB_URL = settings.DB_URL

Base = declarative_base()

engine = create_engine(DB_URL)

session = sessionmaker(bind=engine,
                       autoflush=False,
                       expire_on_commit=False)


def get_session():
    try:
        db = session()
        yield db
    finally:
        db.close()




from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Ensure DB_URL uses an async driver scheme (e.g., postgresql+psycopg:// or postgresql+asyncpg://)
if DB_URL.startswith("postgresql://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# CRITICAL FIX: Use create_async_engine instead of create_engine
engine = create_async_engine(
    DB_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

from typing import AsyncGenerator
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Async dependency providing a transactional database session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()