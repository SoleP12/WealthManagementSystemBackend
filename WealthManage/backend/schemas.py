# API Models of what we send
from pydantic import BaseModel, EmailStr

class WealthManagerBase(BaseModel):
    name: str
    email: EmailStr

class WealthManagerCreate(WealthManagerBase):
    name: str
    email: EmailStr
    hashed_password: str
    net_worth: float

class WealthManagerResponse(WealthManagerBase):
    id: int
    name: str
    email: EmailStr
    net_worth: float

    class Config:
        from_attributes = True

class WealthManagerChange(WealthManagerBase):
    name:str
    email:EmailStr
    net_worth:int


