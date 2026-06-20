# API Models of what we send
from pydantic import BaseModel, EmailStr, Field

class WealthManagerBase(BaseModel):
    name: str = Field(min_length = 1, max_length = 20)
    email: EmailStr = Field(min_length = 1, max_length = 40)

class WealthManagerCreate(WealthManagerBase):
    password: str = Field(min_length = 8)
    net_worth: float

class WealthManagerResponse(WealthManagerBase):
    id: int
    net_worth: float
    class Config:
        from_attributes = True

class WealthManagerChange(WealthManagerBase):
    name:str = Field(min_length = 1, max_length = 20)
    email:EmailStr
    net_worth:float

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None 

