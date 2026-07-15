# API Models of what we send
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class WealthManagerBase(BaseModel):
    name: str = Field(min_length = 1, max_length = 20)
    email: EmailStr = Field(min_length = 1, max_length = 40)

class WealthManagerCreate(WealthManagerBase):
    password: str = Field(min_length = 8)
    net_worth: float

class WealthManagerResponse(WealthManagerBase):
    id: int
    net_worth: float
    total_assets: float
    total_debt: float
    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes = True)

class WealthManagerChange(WealthManagerBase):
    name:str = Field(min_length = 1, max_length = 20)
    email:EmailStr
    net_worth:float
    total_assets: float
    total_debt: float

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None 

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(max_length=120)


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)