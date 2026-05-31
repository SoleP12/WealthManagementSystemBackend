from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WealthManager(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index= True)
    name = Column(String, index = True, nullable=False)
    email = Column(String, unique)
    password = Column(String)
    