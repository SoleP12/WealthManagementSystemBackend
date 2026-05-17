from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class WealthManager(BaseModel):
    email: EmailStr
    username: str

class WealthManager(UserBase):
    password: str

class WealthManager(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True