from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker,create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create a SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
# For PostgreSQL you'd use: postgresql://user:password@postgresserver/db

# Create the SQLAlchemy engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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
