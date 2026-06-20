from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from config import settings


##############################################
# Model Imports
from models import WealthManager
##############################################
# Schema Imports
from schemas import Token, WealthManagerBase, WealthManagerChange, WealthManagerCreate, WealthManagerResponse
##############################################
# Database Imports
from database import Base, engine, get_db
##############################################
# Authentication Imports
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_password_hash, get_current_user

##############################################

router = APIRouter()

############################################# Reusable Dependency Types ################################
CurrentUser = Annotated[WealthManager, Depends(get_current_active_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
########################################################################################################

######################################## Protected API Endpoint ###################################
@router.get("/me", response_model = WealthManagerResponse)
async def get_my_wealthmanager(current_user: CurrentUser):
    return current_user
########################################################################################################


############################################### WealthManager Creation #################################
@router.post("/creation", response_model = WealthManagerResponse, status_code = 201)
async def create_user(wealthmanager: WealthManagerCreate, db: DbSession):
    result = await db.execute(select(WealthManager).where(func.lower(WealthManager.email) == wealthmanager.email.lower()))
    if result.scalars().first():
        raise HTTPException(status_code = 409, detail = "WealthManager Already Exists")

    data = wealthmanager.model_dump()
    data["hashed_password"] = get_password_hash(data.pop("password"))
    wealth_manager = WealthManager(**data)
    db.add(wealth_manager)
    await db.commit()
    await db.refresh(wealth_manager)
    return wealth_manager
#########################################################################################################


############################################### Get Specific WealthManager ##############################
@router.get("/getme/{wealthmanager_id}", response_model = WealthManagerResponse)
async def get_users(wealthmanager_id: int, db:DbSession , current_user: WealthManager = Depends(get_current_active_user)):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized Action")
    result = await db.execute(select(WealthManager).where(WealthManager.id == wealthmanager_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail = "WealthManager ID not found")
    return user
##########################################################################################################


############################################### Deletion Endpoint ########################################
@router.delete("/delete/{wealthmanager_id}" , status_code = 204)
async def delete_wealth_manager(wealthmanager_id: int, db: DbSession, current_user: CurrentUser):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized Action: Deletion of Account Unavailable")
    result = await db.execute(select(WealthManager).where(WealthManager.id == wealthmanager_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exist")
    await db.delete(db_user)
    await db.commit()
##########################################################################################################


############################################### Update WealthManager #####################################
@router.patch("/update/{wealthmanager_id}", response_model = WealthManagerResponse)
async def update_wealth_manager(wealthmanager_id: int,wealthmanager:WealthManagerChange, db:DbSession, current_user: CurrentUser):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized Action: Cannot Update Another User's Account")
    result = await db.execute(select(WealthManager).where(WealthManager.id == wealthmanager_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exist")

    existing_user = await db.execute(select(WealthManager).where(func.lower(WealthManager.email) == wealthmanager.email.lower(), WealthManager.id != wealthmanager_id))
    if existing_user.scalars().first():
        raise HTTPException(status_code = 409, detail = "WealthManager already exists")

    update_data = wealthmanager.model_dump(exclude_unset = True)
    
    for field , value in update_data.items():
        setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user
###########################################################################################################


################################################ Showcase Entire Database ##################################
@router.get("/showcase", response_model = list[WealthManagerResponse])
async def show_all_users(db:DbSession, current_user:CurrentUser):
    result = await db.execute(select(WealthManager))
    return result.scalars().all()
###########################################################################################################
