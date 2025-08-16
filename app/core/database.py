from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# -----------------------
# Database Engine & Session
# -----------------------

# Create database engine using connection URL from settings
engine = create_engine(settings.database_url)

# Session factory (used for dependency injection in FastAPI)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
Base = declarative_base()


# -----------------------
# Dependency
# -----------------------
def get_db():
    """Provide a transactional scope around a series of operations.
    
    This is used as a dependency in FastAPI routes 
    to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
