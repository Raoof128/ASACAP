from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "SOCI Act Compliance Automation Platform"}
