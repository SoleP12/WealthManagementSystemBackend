from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message: Wealth Management | Your Wealth In Your Hands"}


if __name__ == "__main__":
    main()