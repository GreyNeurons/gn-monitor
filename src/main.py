from typing import Annotated
from pydantic import HttpUrl
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome"}

@app.get("/uptime")
async def read_item(url: HttpUrl):
    return {
        "url" : url,
        "accessible": True,
        "response_time": 500
     }
