# source venv/bin/activate
##############################################
# FastApi Creation Imports, Exception Imports
from fastapi import Request
from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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
# Database Imports
from .database import engine

##############################################


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Creation of Template object
templates = Jinja2Templates(directory =BASE_DIR /  "templates")


@app.get("/", name = "Login")
async def default_page(request: Request):
    return templates.TemplateResponse(request, "login.html")





@app.get("/dashboard/{}", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")
