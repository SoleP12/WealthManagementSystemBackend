# source .venv/bin/activate
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
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from guard import SecurityConfig, SecurityMiddleware, SecurityDecorator
##############################################

##############################################
#Router Import
from backend.routers import users
##############################################
# Schema Imports
from backend.schemas import Token
##############################################
from backend.routers import users 
##############################################
# Database Imports
from backend.database import engine, get_db

##############################################
# Authentication Imports
from backend.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash, get_current_user

##############################################

#Lifespan Function
@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()
    
app = FastAPI(lifespan = lifespan)

config = SecurityConfig(
    rate_limit = 10,
    enable_redis = False,

    enable_penetration_detection = False,
    rate_limit_window = 300, # 5 Minutes

    excluded_detection_headers={"referer"},
    custom_error_responses={429: "Rate limit exceeded. Please try again later."},
)

guard_deco = SecurityDecorator(config)
app.add_middleware(SecurityMiddleware, config=config)
app.state.guard_decorator = guard_deco



BASE_DIR = Path(__file__).resolve().parent

app.mount("/static",StaticFiles(directory=BASE_DIR / "static"),name="static"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
############################################### Endpoints ##############################################
app.include_router(users.router, prefix = "/api/users", tags=["WealthManager Testing"])

############################################# Reusable Dependency Type ################################
DbSession = Annotated[AsyncSession, Depends(get_db)]
########################################################################################################

#################################################### App MiddleWare  ###################################
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    response.headers["X-Content-Type-Options"] = "nosniff"

    if "Referrer-Policy" not in response.headers:
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    if request.url.hostname not in ("localhost", "127.0.0.1"):
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains"
        )

    return response
########################################################################################################


##################################### Database Health Endpoint #########################################
@app.get("/health")
@guard_deco.rate_limit(requests=3, window = 300) # 3 requests per 5 minutes
async def health_check(db: DbSession):
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code = 503, detail = "Database Unavailable",
        ) from exc
    return{"status": "healthy"}
########################################################################################################


############################################### Home Page for Wealth Manager ##########################
@app.get("/", name = "Wealth M Home")
@guard_deco.rate_limit(requests=10, window = 300) # 10 requests per 5 minutes
async def default_page(request: Request):
    return templates.TemplateResponse(request=request, name ="index.html")
########################################################################################################

############################################### Login Page for Wealth Manager ##########################
@app.get("/login", name = "Wealth M Login")
@guard_deco.rate_limit(requests=10, window = 300)
async def default_page(request: Request):
    return templates.TemplateResponse(request=request, name = "login.html")
########################################################################################################

################################################ Register Page for Wealth Manager ######################
@app.get("/register", name = "Wealth M Register")
@guard_deco.rate_limit(requests=10, window = 300) # 10 requests per 5 minutes
async def register_page(request: Request):
    return templates.TemplateResponse(request = request, name="register.html")
########################################################################################################

######################################## DashBoard Page for Specific WealthManager #####################
@app.get("/dashboard", name="Wealth M Dashboard Page")
@guard_deco.rate_limit(requests=10, window = 300) # 10 requests per 5 minutes
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request = request, name = "dashboard.html")
########################################################################################################


################################################### Forgot Password Route ###############################
@app.get("/forgot-password", include_in_schema = False)
@guard_deco.rate_limit(requests=4, window = 300) # 4 requests per 5 minutes
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(request = request, name = "forgot_password.html", context = {"request": request, "title": "Forgot Password"})
########################################################################################################


################################################### Reset Password Page ###################################################
@app.get("/reset-password", include_in_schema = False)
@guard_deco.rate_limit(requests=4, window = 300) # 4 requests per 5 minutes
async def reset_password_page(request: Request):
    response = templates.TemplateResponse(request = request, name = "reset_password.html", context = {"request": request, "title": "Reset Password"})
    response.headers["Referrer-Policy"] = "no-referrer"
    return response
########################################################################################################


################################################### Token Creation Endpoint #######################################
@app.post("/token", response_model = Token)
@guard_deco.rate_limit(requests=5, window = 300) # 5 requests per 5 minutes
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:DbSession ):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username or password", headers = {"WWW-Authenticate": "Bearer"},)
    access_token = create_access_token(
        data = {"sub": user.email},
        expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token = access_token, token_type = "bearer")
###########################################################################################################

