# source venv/bin/activate
##############################################
# FastApi Creation Imports, Exception Imports
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

##############################################
from pathlib import Path
from fastapi.staticfiles import StaticFiles

##############################################
# Import To Run Server
import uvicorn

##############################################
# Model Imports
# from models import models
from models import WealthManager

##############################################
# Schema Import
from schemas import WealthManagerResponse, WealthManagerCreate, WealthManagerBase, WealthManagerChange

##############################################
# Database Imports
from database import Base, engine, get_db

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


###################### Endpoints ##############################################
@app.get("/login/", name = "Login")
async def default_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

# Creation of WealthManager
@app.post("/wealthmanager/", response_model = WealthManagerResponse)
async def create_user(wealthmanager: WealthManagerCreate, db:Session = Depends(get_db)):
    if db.query(WealthManager).filter(WealthManager.email == wealthmanager.email).first():
        raise HTTPException(status_code = 404, detail = "WealthManager Already Exists")
    # Creation of New Wealth Manager
    wealth_manager = WealthManager(**wealthmanager.dict())
    db.add(wealth_manager)
    db.commit()
    db.refresh(wealth_manager)
    return wealth_manager

# Get Specific WealthManager
@app.get("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def get_users(wealthmanager_id: int, db:Session = Depends(get_db)):
    user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    return user

    if not user:
        raise HTTPException(status_code=404, detail = "WealthManager ID not found")

@app.get("/wealthmanager/" , response_model = WealthManagerResponse)
async def delete_wealth_manager(db:Session = Depends(get_db)):
    pass

# Update Users
@app.post("/wealthmanager/{wealthmanager_id}", response_model = WealthManagerResponse)
async def update_wealth_manager(wealthmanager_id: int,wealthmanager:WealthManagerChange, db:Session = Depends(get_db)):
    db_user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail = "WealthManager Does not Exists")

    for field , value in wealthmanager.dict().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user







# Showcase all wealth managers in database
@app.get("/allWealthManagers/")
async def show_all_users(db:Session = Depends(get_db)):
    for users in db.query(WealthManager):
        return users

    if not db.query(WealthManager):
        raise HTTPException(status_code = 404, detail = "No WealthManagers in Database")

# Specific Wealth Manager Dashboard
@app.get("/dashboard/{wealthmanager_id}", response_class=HTMLResponse)
async def dashboard_page(wealthmanager_id : int ,request: Request):
    return templates.TemplateResponse(request, "dashboard.html")
