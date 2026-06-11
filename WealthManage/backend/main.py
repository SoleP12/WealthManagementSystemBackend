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
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_password_hash

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


############################################### Login Page for Wealth Manager ##########################
@app.get("/", name = "WealthMLogin", response_model = WealthManagerCreate)
async def default_page(request: Request):
    return templates.TemplateResponse(request, "login.html")
########################################################################################################


######################################## DashBoard Page for Specific WealthManager #####################
@app.get("login/dashboard/{wealthmanager_id}", response_model=WealthManagerResponse)
async def dashboard_page(wealthmanager_id : int ,request: Request):
    return templates.TemplateResponse(request, "dashboard.html")
########################################################################################################


############################################### WealthManager Creation #################################
@app.post("/wealthmanager/", response_model = WealthManagerResponse)
async def create_user(wealthmanager: WealthManagerCreate, db:Session = Depends(get_db)):
    if db.query(WealthManager).filter(WealthManager.email == wealthmanager.email).first():
        raise HTTPException(status_code = 409, detail = "WealthManager Already Exists")

    data = wealthmanager.dict()
    data["hashed_password"] = get_password_hash(data["hashed_password"])
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
        raise HTTPException(status_code = 403, detail = "")
    user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not user:
        raise HTTPException(status_code=404, detail = "WealthManager ID not found")
    return user
##########################################################################################################


############################################### Deletion Endpoint ########################################
@app.delete("/wealthmanager/{wealthmanager_id}" , status_code = 204)
async def delete_wealth_manager(wealthmanager_id: int, db:Session = Depends(get_db), current_user: WealthManager = Depends(get_current_active_user)):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "")
    db_user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exists")

    db.delete(db_user)
    db.commit()
##########################################################################################################


############################################### Update WealthManager #####################################
@app.patch("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def update_wealth_manager(wealthmanager_id: int,wealthmanager:WealthManagerChange, db:Session = Depends(get_db), current_user: WealthManager = Depends(get_current_active_user)):
    if current_user.id != wealthmanager_id:
        raise HTTPException(status_code = 403, detail = "")
    db_user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exists")

    update_data = wealthmanager.dict(exclude_unset = True)
    for field , value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user
###########################################################################################################


################################################ Showcase Entire Database ##################################
@app.get("/allWealthManagers/", response_model = list[WealthManagerResponse])
async def show_all_users(db:Session = Depends(get_db)):
        return db.query(WealthManager).all()
###########################################################################################################


################################################### Token Creation Endpoint #######################################
@app.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(get_db), ):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username or password", headers = {"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(
        data = {"sub": user.email},
        expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token = access_token, token_type = "bearer")
###########################################################################################################