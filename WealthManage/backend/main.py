# source venv/bin/activate
##############################################
# FastApi Creation Imports, Exception Imports
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

##############################################
from pathlib import Path
from fastapi.staticfiles import StaticFiles

##############################################
# Import To Run Server
import uvicorn

##############################################
# Model Imports
from . import models
from .models import WealthManager

##############################################
# Schema Import
from .schemas import WealthManagerResponse, WealthManagerCreate, WealthManagerBase

##############################################
# Database Imports
from .database import Base, engine, get_db

##############################################

Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Creation of Template object
templates = Jinja2Templates(directory =BASE_DIR /  "templates")



###################### Endpoints ##############################################
@app.get("/", name = "Login")
async def default_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

# Creation of WealthManager
@app.post("/wealthmanager/", response_model = WealthManagerResponse)
def create_user(wealthmanager: WealthManagerCreate, db:Session = Depends(get_db)):
    if db.query(WealthManager).filter(WealthManager.email == wealthmanager.email).first():
        raise HTTPException(status_code = 404, detail = "WealthManager Already Exisit")
    # Creation of New Wealth Manager
    wealth_manager = WealthManager(**wealthmanager.dict())
    db.add(wealth_manager)
    db.commit()
    db.refresh(wealth_manager)
    return wealth_manager

# Get Specific WealthManager
@app.get("/users/{wealthmanager_id}", response_model = WealthManagerResponse)
def get_users(wealthmanager_id: int, db:Session = Depends(get_db)):
    user = db.query(WealthManager).filter(WealthManager.id == wealthmanager_id).first()
    if not user:
        raise HTTPException(status_code=404, detail = "WealthManager not found")



@app.get("/allWealthManagers/")
def showcasedatabase():
    db.query(WealthManager)





@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")
