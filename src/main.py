from fastapi import FastAPI
from .config import settings
from .routes import api_router
from .db import create_db_and_tables


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
