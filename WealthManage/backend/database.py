from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker,create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import settings


# Create the SQLAlchemy engine
engine = create_async_engine(
    settings.database_url
)
# The connect_args is needed only for SQLite. For other databases, it's not required.

# Create a SessionLocal class
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

# Create a Base class
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
