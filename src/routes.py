# TODO : refactor later like
# full-stack-fastapi-template/backend/app/api/main.py
from typing import Any
from fastapi import APIRouter
from pydantic import HttpUrl
from sqlmodel import select, Session
from .lib.check_access import access_url
from .lib.check_domain import get_domain_expiry_date
from .lib.check_ssl import check_ssl
from .models import User, UrlPublic, UrlsPublic, Url, UrlCreate
from .db import engine


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


# After integrating auth, we do not need owner email
# We get the user directly from the auth token
@api_router.get("/urls", response_model=UrlsPublic)
async def get_urls(owner_email: str, skip: int = 0, limit: int = 100) -> Any:
    """
    Get the URLs
    """
    urls = []
    count = 0

    with Session(engine) as session:
        statement = (
            select(User)
            # .where(Url.owner == current_user.id)
            .where(User.email == owner_email)
            .offset(skip)
            .limit(limit)
        )
        results = session.exec(statement).all()
        urls = [{"id": u.id, "url": u.url} for r in results for u in r.urls]
        count = len(urls)

    return UrlsPublic(data=urls, count=count)


@api_router.post("/url", response_model=UrlPublic)
# async def add_url(owner_email: str, new_url: UrlCreate) -> Any:
async def add_url(new_url: UrlCreate) -> Any:
    """
    Add a URL
    """
    with Session(engine) as session:
        url = Url.model_validate(new_url)
        session.add(url)
        session.commit()
        session.refresh(url)
        return url
