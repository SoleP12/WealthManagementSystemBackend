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
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
##############################################

##############################################
#Router Import
from routers import users
##############################################
# Schema Imports
from schemas import Token
##############################################
from routers import users 
##############################################
# Database Imports
from database import Base, engine, get_db

##############################################
# Authentication Imports
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_password_hash, get_current_user

##############################################

#Lifespan Function
@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
    yield
    await engine.dispose()

app = FastAPI(lifespan = lifespan)

BASE_DIR = Path(__file__).resolve().parent
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Creation of Template object For FrontEnd of Service
templates = Jinja2Templates(directory =BASE_DIR /  "templates")

############################################### Endpoints ##############################################
app.include_router(users.router, prefix = "/WealthM/wealthmanager", tags=["WealthManagers"])

############################################# Reusable Dependency Type ################################
DbSession = Annotated[AsyncSession, Depends(get_db)]

########################################################################################################


############################################### Login Page for Wealth Manager ##########################
@app.get("/", name = "WealthM")
async def default_page(request: Request):
    return templates.TemplateResponse(request, "login.html")
########################################################################################################
@app.post("/register", name = "WealthMRegister")
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")
######################################## DashBoard Page for Specific WealthManager #####################
@app.get("/dashboard/{wealthmanager_id}")
async def dashboard_page(wealthmanager_id: int, request: Request, current_user: WealthManager = Depends(get_current_active_user)):
    return templates.TemplateResponse(request = request, name = "dashboard.html")
########################################################################################################

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

