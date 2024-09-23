from sqlmodel import SQLModel, create_engine
from .config import settings

engine = create_engine(settings.DATABASE_URL.unicode_string(), echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
