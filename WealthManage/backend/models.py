from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from pydantic import BaseModel
from database import Base




class WealthManager(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
