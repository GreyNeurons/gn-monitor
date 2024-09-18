from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from .config import settings
from .routes import api_router


def create_db_and_tables():
    engine = create_engine(settings.DATABASE_URL.unicode_string(), echo=True)
    SQLModel.metadata.create_all(engine)


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
