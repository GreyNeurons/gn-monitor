# Refer to https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/models.py

import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    urls: list["Url"] = Relationship(back_populates="owner", cascade_delete=True)


# Shared properties
class UrlBase(SQLModel):
    url: str = Field(min_length=5, max_length=255)


# Properties to receive on item creation
class UrlCreate(UrlBase):
    pass


# Properties to receive on item update
class UrlUpdate(UrlBase):
    url: str


# Database model, database table inferred from class name
class Url(UrlBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="urls")
