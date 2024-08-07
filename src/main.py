from pydantic import HttpUrl
from fastapi import FastAPI
from check_access import access_url

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/reachable")
async def read_item(url: HttpUrl):
    accesible, resp_time, is_secure = access_url(url)
    return {
        "url": url,
        "accessible": accesible,
        "response_time": resp_time,
        "is_secure": is_secure,
    }
