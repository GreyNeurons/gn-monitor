# Refer to https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/models.py
import enum
import uuid
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Column, Enum, Field, JSON, Relationship, SQLModel


class Status(str, enum.Enum):
    all_ok = "all_ok"


class BaseModel(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_edited: datetime = Field(default_factory=datetime.utcnow,
                                  nullable=False)


# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    urls: list["Url"] = Relationship(back_populates="owner",
                                     cascade_delete=True)


# Shared properties
class UrlBase(BaseModel):
    url: str = Field(min_length=5, max_length=255)


# Properties to receive on item creation
class UrlCreate(UrlBase):
    owner_email: str  # Eventually this goes away ??
    # pass


# Properties to receive on item update
class UrlUpdate(SQLModel):
    owner_email: str  # Eventually this goes away ??
    url: str


# Properties to return via API, id is always required
class UrlPublic(UrlBase):
    id: uuid.UUID
    # url: str


class UrlsPublic(SQLModel):
    data: list[UrlPublic]
    count: int


# Database model, database table inferred from class name
class Url(UrlBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    url: str = Field(max_length=255)
    # owner_id: uuid.UUID = Field(
    #     foreign_key="user.id", nullable=False, ondelete="CASCADE"
    # )
    owner_email: str = Field(
        foreign_key="user.email", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="urls")


# Shared properties
class UrlStatusBase(BaseModel):
    status: Status = Field(sa_column=Column(Enum(Status)))
    description: dict = Field(default_factory=dict, sa_column=Column(JSON))

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
