# API Models of what we send
from pydantic import BaseModel, EmailStr

class WealthManagerBase(BaseModel):
    name: str
    email: EmailStr

class WealthManagerCreate(WealthManagerBase):
    name: str
    email: EmailStr
    password: str

class WealthManagerResponse(WealthManagerBase):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True