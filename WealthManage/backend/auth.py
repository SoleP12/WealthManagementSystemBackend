from datetime import datetime, timedelta, timezone
from typing import Annotated
from config import SECRET_KEY

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exception import Invalid TokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from schemas import TokenData
from database import get_db 
from models import WealthManager


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
fake_hash = password_hash.hash("fakehash")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def authenticate_user(db: Session, email: str, password:str):
    user = db.query(WealthManager).filter(WealthManager.email == email).first()
    if not user:
        verify_password(password, fake_hash)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) ->str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes = 15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


