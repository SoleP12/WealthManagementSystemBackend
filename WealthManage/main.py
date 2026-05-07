from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Creation of Template object
templates = Jinja2Templates(directory = "templates")








@app.get("/")
async def root():
    return {"message: Wealth Management | Your Wealth In Your Hands"}


if __name__ == "__main__":
    main()