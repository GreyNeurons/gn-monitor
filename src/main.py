from pydantic import HttpUrl
from fastapi import FastAPI
from lib.check_access import access_url
from lib.check_domain import get_domain_expiry_date
from lib.check_ssl import check_ssl


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/reachable")
async def read_item(url: HttpUrl):
    accesible, resp_time, is_secure = access_url(url)

    data = {
        "url": url,
        "accessible": accesible,
        "response_time": resp_time,
        "is_secure": is_secure,
    }

    expiry_date = get_domain_expiry_date(url)
    if expiry_date:
        data["expiry_date"] = expiry_date

    _, ssl_msg = check_ssl(url)
    if ssl_msg:
        data["ssl_msg"] = ssl_msg

    return data
