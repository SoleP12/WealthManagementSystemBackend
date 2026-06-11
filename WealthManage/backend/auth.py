##############################################
# Standard Library Imports
from datetime import datetime, timedelta, timezone
from typing import Annotated

##############################################
# Third-Party Imports
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session


##############################################
# Configuration Imports
from config import SECRET_KEY

##############################################
# Database Imports
from database import get_db

##############################################
# Model Imports
from models import WealthManager

##############################################
# Schema Imports
from schemas import TokenData

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
fake_hash = password_hash.hash("fakehash")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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

async def get_current_user(token : Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exeception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = {"WWWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exeception
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credentials_exeception
    user = db.query(WealthManager).filter(WealthManager.email == token_data.username).first()
    if user is None:
        raise credentials_exeception
    return user

async def get_current_active_user(current_user: Annotated[WealthManager, Depends(get_current_user)]):
    if getattr(current_user, "disabled", False):
        raise HTTPException(status_code = 400, detail = "Inactive user")
    return current_user