"""
This is the database module.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./app/data.db"

# Create the database engine
engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

# Create a session local object for database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


def get_db():
    """
    Gets a connection to the database and yields it so that it can be used in routes.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()