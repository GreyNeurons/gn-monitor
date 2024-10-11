# TODO : refactor later like
# full-stack-fastapi-template/backend/app/api/main.py
import uuid
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl
from sqlmodel import select, Session
from .lib.check_access import access_url
from .lib.check_domain import get_domain_expiry_date
from .lib.check_ssl import check_ssl
from .models import (
    User,
    UrlPublic,
    UrlsPublic,
    Url,
    UrlCreate,
    UrlUpdate,
    UserCreateRequest,
    SignInRequest,
    ResetPasswordRequest,
    LogOutRequest,
)
from .db import engine
from .lib.auth import create_user, sign_in, get_user_roles, reset_password, log_out
from keycloak import KeycloakError


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
@api_router.get("/urls", response_model=UrlsPublic, summary="Get the list of URLs for the user", tags=["URL"])
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


@api_router.post("/url", response_model=UrlPublic, summary="Add URL for a user", tags=["URL"])
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


@api_router.put("/url/{id}", response_model=UrlPublic, summary="Update URL", tags=["URL"])
async def update_url(id: uuid.UUID, url_in: UrlUpdate) -> Any:
    """
    Update the URL.
    """
    with Session(engine) as session:
        url = session.get(Url, id)
        if not url:
            raise HTTPException(status_code=404, detail="Item not found")
        update_dict = url_in.model_dump(exclude_unset=True)
        url.sqlmodel_update(update_dict)
        session.add(url)
        session.commit()
        session.refresh(url)
        return url


@api_router.post("/create_user", summary="Create User", tags=["Authentication"])
async def api_create_user(request: UserCreateRequest):
    try:
        user_id = create_user(
            request.username,
            request.password,
            request.first_name,
            request.last_name,
            request.email,
        )
        return {"user_id": user_id}
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/sign_in", summary="Sign In", tags=["Authentication"])
async def api_sign_in(request: SignInRequest):
    try:
        token = sign_in(request.username, request.password)
        return token
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.get("/get_user_roles/{user_id}", summary="Get User Roles", tags=["Authentication"])
async def api_get_user_roles(user_id: str):
    try:
        roles = get_user_roles(user_id)
        return roles
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/reset_password", summary="Reset Password", tags=["Authentication"])
async def api_reset_password(request: ResetPasswordRequest):
    try:
        reset_password(request.user_id, request.new_password)
        return {"detail": "Password reset successful"}
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/log_out", summary="Log out", tags=["Authentication"])
async def api_log_out(request: LogOutRequest):
    try:
        log_out(request.refresh_token)
        return {"detail": "User logged out successfully"}
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))
