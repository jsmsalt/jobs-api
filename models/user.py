from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from pydantic import EmailStr
from sqlalchemy import String, Column
from sqlmodel import Field, Relationship
from models.base import BaseModel, BaseTableFields


if TYPE_CHECKING:
    from models.session import Session
    from models.role import Role
    from models.job import Job


class User(BaseModel, BaseTableFields, table=True):
    __tablename__ = "users"

    password: str = Field(
        sa_column=Column(
            String,
            nullable=False
        )
    )
    username: str = Field(
        sa_column=Column(
            String(50),
            unique=True,
            nullable=False
        )
    )
    email: EmailStr = Field(
        sa_column=Column(
            String,
            unique=True,
            nullable=False
        )
    )
    first_name: Optional[str] = Field(sa_column=Column(String, nullable=True))
    last_name: Optional[str] = Field(sa_column=Column(String, nullable=True))

    role_id: int = Field(foreign_key="roles.id")
    role: "Role" = Relationship(back_populates="users")
    sessions: List["Session"] = Relationship(back_populates="user")
    jobs: List["Job"] = Relationship(back_populates="user")


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


# Related Schemas

class UserSession(BaseModel):
    user_id: int
    role: str
    permissions: List[str]


class UserCredentials(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str
