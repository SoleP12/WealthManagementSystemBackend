from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create a SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# For PostgreSQL you'd use: postgresql://user:password@postgresserver/db

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# The connect_args is needed only for SQLite. For other databases, it's not required.

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
get_db()
