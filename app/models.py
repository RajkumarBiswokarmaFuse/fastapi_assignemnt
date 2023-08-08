"""
    This is a model.
"""
from sqlalchemy import Column, String
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from app.database import Base


class Employee(Base):
    """
    Data model for Employee.
    """
    __tablename__ = 'employee'

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
