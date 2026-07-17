from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import select, func
from sqlalchemy import delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, UTC, datetime
from backend.config import settings


##############################################
# Model Imports
from backend.models import WealthManager,PasswordResetToken
##############################################
# Schema Imports
from backend.schemas import Token, WealthManagerBase, WealthManagerChange, WealthManagerCreate, WealthManagerResponse, ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest
##############################################
# Database Imports
from backend.database import Base, engine, get_db
##############################################
# Authentication Imports
from backend.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_password_hash, get_current_user, generate_reset_token,hash_reset_token, verify_password

##############################################
#Email Utils Import
from backend.email_utils import send_password_reset_email
##############################################
router = APIRouter()

############################################# Reusable Dependency Types ################################
CurrentUser = Annotated[WealthManager, Depends(get_current_active_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
########################################################################################################


############################################### WealthManager Creation #################################
@router.post("/creation", response_model = WealthManagerResponse, status_code = 201)
async def create_user(wealthmanager: WealthManagerCreate, db: DbSession):
    result = await db.execute(select(WealthManager).where(func.lower(WealthManager.email) == wealthmanager.email.lower()))
    if result.scalars().first():
        raise HTTPException(status_code = 409, detail = "WealthManager Already Exists")

    data = wealthmanager.model_dump()

    data["net_worth"] = (
        data["total_assets"] - data["total_debt"]
    )

    data["hashed_password"] = get_password_hash(data.pop("password"))
    wealth_manager = WealthManager(**data)
    
    db.add(wealth_manager)
    await db.commit()
    await db.refresh(wealth_manager)
    return wealth_manager
#########################################################################################################


######################################## Protected API Endpoint To Return User Info ###################################
@router.get("/me", response_model = WealthManagerResponse)
async def get_my_wealthmanager(current_user: CurrentUser, db: DbSession):
    return current_user
########################################################################################################


######################################## Forgot Password Endpoint ######################################
@router.post("/forgot-password", status_code = 202)
async def forgot_password(request_data: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: DbSession):
    result = await db.execute(select(WealthManager).where(func.lower(WealthManager.email) == request_data.email.lower()))
    user = result.scalars().first()
    if user:
        await db.execute(sql_delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id))

        token = generate_reset_token()
        token_hash = hash_reset_token(token)
        expires_at = datetime.now(UTC) + timedelta(minutes=settings.reset_token_expire_minutes)

        reset_token = PasswordResetToken(user_id = user.id, token_hash = token_hash, expires_at=expires_at)
        db.add(reset_token)
        await db.commit()

        background_tasks.add_task(send_password_reset_email, to_email = user.email, username =user.email, token = token)
        return{"message":"If an account exists with this email, you will recieve password reset instructions."}
########################################################################################################


######################################## Users Logged In Can Reset Password ############################
@router.patch("/me/password", status_code = 200)
async def change_password(password_data: ChangePasswordRequest, current_user:CurrentUser, db:DbSession):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code = 400, detail = "Current password is incorrect")
    
    current_user.hashed_password = get_password_hash(password_data.new_password)

    await db.execute(sql_delete(PasswordResetToken).where(PasswordResetToken.user_id == current_user.id))
    await db.commit()
    return {"message": "Password changed successfully"}
########################################################################################################


######################################## Reset Password Endpoint #######################################
@router.post("/reset-password", status_code = 200)
async def reset_password(request_data: ResetPasswordRequest, db: DbSession):
    token_hash = hash_reset_token(request_data.token)

    result = await db.execute(select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash))

    reset_token = result.scalars().first()
    if not reset_token:
        raise HTTPException(status_code = 400, detail = "Invalid or Expired Token")
    
    if reset_token.expires_at  < datetime.now(UTC):
        await db.delete(reset_token)
        await db.commit()
        raise HTTPException(status_code = 400, detail = "Invalid or Expired Token")
    
    result = await db.execute(select(WealthManager).where(WealthManager.id == reset_token.user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code = 400, detail="Invalid or Expired Token")
    
    user.hashed_password = get_password_hash(request_data.new_password)

    await db.execute(sql_delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id))

    await db.commit()
    return{"message": "Password reset successfully. You can now login with your new password."}
########################################################################################################


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
@router.patch("/update/{wealthmanager_id}", response_model = WealthManagerResponse, response_model_exclude_unset = True)
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
        if getattr(db_user,field) != value:
            setattr(db_user, field, value)

    db_user.net_worth = (
        db_user.total_assets - db_user.total_debt
    )

    await db.commit()
    await db.refresh(db_user)
    return db_user
###########################################################################################################

################################################ Showcase Entire Database ##################################
@router.get("/showcase", response_model = list[WealthManagerResponse])
async def show_all_users(db:DbSession): #current_user:CurrentUser
    result = await db.execute(select(WealthManager))
    return result.scalars().all()
###########################################################################################################
