# TODO : refactor later like
# full-stack-fastapi-template/backend/app/api/main.py

from fastapi import APIRouter
from pydantic import HttpUrl
from .lib.check_access import access_url
from .lib.check_domain import get_domain_expiry_date
from .lib.check_ssl import check_ssl

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"message": "Welcome"}


@api_router.get("/reachable")
async def url_reachable(url: HttpUrl):
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
