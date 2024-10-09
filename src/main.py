from pydantic import BaseModel,HttpUrl
from fastapi import FastAPI
from lib.check_access import access_url
from lib.check_domain import get_domain_expiry_date
from lib.check_ssl import check_ssl
from lib.auth import *


app = FastAPI()

# Request models
class UserCreateRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str

class SignInRequest(BaseModel):
    username: str
    password: str

class ResetPasswordRequest(BaseModel):
    user_id: str
    new_password: str

class LogOutRequest(BaseModel):
    refresh_token: str



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

@app.post("/create_user")
async def api_create_user(request: UserCreateRequest):
    try:
        user_id = create_user(request.username, request.password, request.first_name, request.last_name, request.email)
        return {"user_id": user_id}
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sign_in")
async def api_sign_in(request: SignInRequest):
    try:
        token = sign_in(request.username, request.password)
        return token
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_user_roles/{user_id}")
async def api_get_user_roles(user_id: str):
    try:
        roles = get_user_roles(user_id)
        return roles
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset_password")
async def api_reset_password(request: ResetPasswordRequest):
    try:
        reset_password(request.user_id, request.new_password)
        return {"detail": "Password reset successful"}
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/log_out")
async def api_log_out(request: LogOutRequest):
    try:
        log_out(request.refresh_token)
        return {"detail": "User logged out successfully"}
    except KeycloakError as e:
        raise HTTPException(status_code=400, detail=str(e))

