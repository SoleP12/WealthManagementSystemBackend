from sqlalchemy import Column, String, Integer, Float
from database import Base


class WealthManager(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index= True)
    name = Column(String, index = True, nullable=False)
    email = Column(String, unique = True)
    password = Column(String, nullable = False)
    net_worth = Column(Float, default = 0.0)
    