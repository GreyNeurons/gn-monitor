from fastapi import FastAPI
from pydantic import HttpUrl
from sqlmodel import SQLModel, create_engine
from .config import settings
from .lib.check_access import access_url
from .lib.check_domain import get_domain_expiry_date
from .lib.check_ssl import check_ssl


def create_db_and_tables():
    engine = create_engine(settings.database_url)
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    
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
