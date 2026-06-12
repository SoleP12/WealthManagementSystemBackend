# source venv/bin/activate
##############################################
# Standard Library Imports
from datetime import timedelta
from pathlib import Path
from typing import Annotated

##############################################
# Third-Party Imports
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

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

Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Creation of Template object For FrontEnd of Service
templates = Jinja2Templates(directory =BASE_DIR /  "templates")

############################################### Endpoints ##############################################


############################################# Reusable Dependency Types ################################
CurrentUser = Annotated[WealthManager, Depends(get_current_active_user)]
DbSession = Annotated[Session, Depends(get_db)]
########################################################################################################


############################################### Login Page for Wealth Manager ##########################
@app.get("/", name = "WealthMLogin")
async def default_page(request: Request):
    return templates.TemplateResponse(request, "login.html")
########################################################################################################


######################################## DashBoard Page for Specific WealthManager #####################
@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request = request, name = "dashboard.html")
########################################################################################################


######################################## Protected API Endpoint ###################################
@app.get("/wealthmanager/me", response_model = WealthManagerResponse)
async def get_my_wealthmanager(current_user: CurrentUser):
    return current_user
########################################################################################################


############################################### WealthManager Creation #################################
@app.post("/wealthmanager/", response_model = WealthManagerResponse, status_code = 201)
async def create_user(wealthmanager: WealthManagerCreate, db: DbSession):
    if db.query(WealthManager).filter(WealthManager.email == wealthmanager.email).first():
        raise HTTPException(status_code = 409, detail = "WealthManager Already Exists")

    data = wealthmanager.model_dump()
    data["hashed_password"] = get_password_hash(data.pop("password"))
    wealth_manager = WealthManager(**data)
    db.add(wealth_manager)
    db.commit()
    db.refresh(wealth_manager)
    return wealth_manager
#########################################################################################################


############################################### Get Specific WealthManager ##############################
@app.get("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def get_users(wealthmanager_id: int, db:Session = Depends(get_db), current_user: WealthManager = Depends(get_current_active_user)):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized Action")
    user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not user:
        raise HTTPException(status_code=404, detail = "WealthManager ID not found")
    return user
##########################################################################################################


############################################### Deletion Endpoint ########################################
@app.delete("/wealthmanager/{wealthmanager_id}" , status_code = 204)
async def delete_wealth_manager(wealthmanager_id: int, db: DbSession, current_user: CurrentUser):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized Action: Deletion of Account Unavailable")
    db_user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exist")
    db.delete(db_user)
    db.commit()
##########################################################################################################


############################################### Update WealthManager #####################################
@app.patch("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def update_wealth_manager(wealthmanager_id: int,wealthmanager:WealthManagerChange, db:DbSession, current_user: CurrentUser):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "Unauthorized Action: Cannot Update Another User's Account")
    db_user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exist")

    update_data = wealthmanager.model_dump(exclude_unset = True)
    for field , value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user
###########################################################################################################


################################################ Showcase Entire Database ##################################
@app.get("/allWealthManagers/", response_model = list[WealthManagerResponse])
async def show_all_users(db:DbSession, current_user:CurrentUser):
        return db.query(WealthManager).all()
###########################################################################################################


################################################### Token Creation Endpoint #######################################
@app.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:DbSession ):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username or password", headers = {"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(
        data = {"sub": user.email},
        expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token = access_token, token_type = "bearer")
###########################################################################################################