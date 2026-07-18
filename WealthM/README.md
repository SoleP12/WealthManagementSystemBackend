# Wealth Management System Backend
# Primary Purpose:
The objective of this Personal Project is to demonstrate modern backend Software Engineering principles and practices through a personal project. If there are any suggestions or faults that you see within the project please let me know I'm always oopen to learning and improving

## *Features:
    - Secure user registration and authentication using JWT
    - Password hashing for secure credential storage
    - Password reset functionality via email
    - CRUD operations for user financial information
    - Track:
        - Net Worth
        - Total Assets
        - Total Debts
    - Asynchronous API built with FastAPI
    - PostgreSQL database with SQLAlchemy ORM
    - Alembic database migrations
    - Docker support for containerized deployment
    - Automated API testing with Pytest
    - Environment variable configuration using Pydantic Settings
    - Security headers for improved application security

## *Tech Stack:
    Backend
        - Python 3.14
        - FastAPI 0.139.2
        - SQAlchemy 2.0
        - PostgreSQL 18.4
        - Alembic 1.18.5
        - Pydantic v2
        - Uvicorn 0.51.0
    
    Authentication & Safety
        - JWT Authentication
        - Password Hashing
        - OAuth2 Password Flow
        - Security HTTp Headers

    Testing
        - Pytest
        - HTTPX
        - AnyIO

    DevOps
        - Docker
        - Git
        - GitHub

## *Configure Environment Variables:
    .env file -- Configure These Environment varibales
        -Create ".env.py"
        -Add these variables to the python file
            - DATABASE_URL=your_database_url 
                - Example: " postgresql+psycopg://{user}:{password}@localhost/{databasename} "
            - SECRET_KEY=your_secret_key (Generate with "openssl rand -hex 32" paste into terminal)
            - MAIL_SERVER= (Used mailtrap.io to test for user emails) 
            - MAIL_PORT= (Used mailtrap.io to test for user emails)
            - MAIL_USERNAME= (Used mailtrap.io to test for user emails)
            - MAIL_PASSWORD= (Used mailtrap.io to test for user emails)
            - MAIL_FROM= (Used mailtrap.io to test for user emails)
            - ACCESS_TOKEN_EXPIRE_MINUTES=30 
            - RESET_TOKEN_EXPIRE_MINUTES=15 
    *Do not space after pasting ensure ....=bjsbksjbfkjbfksjf not .... = jfskfjhksfhksf or ....= kfjkfsjfnskfksfn

## *Running Locally:
    * " git clone https://github.com/SoleP12/WealthManagementSystemBackend.git "
    * Change Directory to WealthManage Folder -- cd WealthM --
    * Create Virtual Enviroment Using python3 -m venv {NAME OF YOUR VIRTUAL ENVIRONMENT}
    * Activate Virtual Your Enviroment
    * PIP or Uvicorn intstall the requiremnets.txt with -- "pip install -r requirements.txt" -- or -- "uv add -r requirements.txt" --
    * Change the Directory to the WealthM Folder using "cd WealthM"
    * Run Website With -- "uvicorn backend.main:app --reload" in WealthM folder

## *Running Docker:
    - Ensure Docker is running first on your machine
    - Build the image: -- " docker build wealth-m-api . " --
    - Run Container:  -- " docker run -p 8000:8000 --env-file wealth-m-api "
    - Stop Container -- " docker stop wealth-m-api "

## *Testing:
    - Run postgres first locally on your machine
    - Start -- " brew services start postgresql " if installed with HOMEBREW
    - " cd WealthM "
    - Run Tests with " pytest tests/tests_users.py -s " 
    - Stop -- " brew services stop postgresql " if installed with HOMEBREW

## *Alembic Usage:
    - Create a migration:
        - alembic revision --autogenerate -m "message"
    - Use Migration:
        - alembic upgrade head

## *Database Shema(As of July 16th)
id | email | hashed_pass | net_worth | name | phone_number | created_at | total_assets | total_debt | pass_reset_token 
---|-------|-------------|-----------|------|--------------|------------|--------------|------------|-----------------
   |       |             |           |      |              |            |              |            | 
   |       |             |           |      |              |            |              |            |


