# source venv/bin/activate
##############################################
# FastApi Creation Imports, Exception Imports
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import timedelta
from typing import Annotated
##############################################
from pathlib import Path
from fastapi.staticfiles import StaticFiles

##############################################
# Import To Run Server
import uvicorn

##############################################
# Model Imports
from models import WealthManager

##############################################
# Schema Import
from schemas import WealthManagerResponse, WealthManagerCreate, WealthManagerBase, WealthManagerChange
from schemas import Token

##############################################
# Database Imports
from database import Base, engine, get_db

##############################################
# Auth Imports
from auth import authenticate_user, create_access_token, get_current_active_user,get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES

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
@app.get("/", name = "Login", response_model = WealthManagerCreate)
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
        raise HTTPException(status_code = 404, detail = "WealthManager Already Exists")

    wealth_manager = WealthManager(**wealthmanager.dict())
    db.add(wealth_manager)
    db.commit()
    db.refresh(wealth_manager)
    return wealth_manager
#########################################################################################################


############################################### Get Specific WealthManager ##############################
@app.get("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def get_users(wealthmanager_id: int, db:Session = Depends(get_db)):
    user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    return user
    if not user:
        raise HTTPException(status_code=404, detail = "WealthManager ID not found")
##########################################################################################################


############################################### Deletion Endpoint ########################################
@app.delete("/wealthmanager/{wealthmanager_id}" , status_code = 204)
async def delete_wealth_manager(wealthmanager_id: int, db:Session = Depends(get_db)):
    db_user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exists")

    db.delete(db_user)
    db.commit()
##########################################################################################################


############################################### Update WealthManager #####################################
@app.patch("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def update_wealth_manager(wealthmanager_id: int,wealthmanager:WealthManagerChange, db:Session = Depends(get_db)):
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
    if Session:
        return db.query(WealthManager).all()
    else:
        raise HTTPException(status_code = 404 , detail = "Database Creation Has Not Been Implemented")
###########################################################################################################




###########################################################################################################
