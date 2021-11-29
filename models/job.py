from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from models.base import BaseModel, BaseTableFields
from sqlmodel import Field, Relationship, String, Column

if TYPE_CHECKING:
    from models.user import User


class Job(BaseModel, BaseTableFields, table=True):
    __tablename__ = "jobs"

    title: str = Field(sa_column=Column(String(100), nullable=False))
    text: str = Field(sa_column=Column(String, nullable=False))
    location: str = Field(sa_column=Column(String(100), nullable=False))

    user_id: Optional[int] = Field(foreign_key="users.id", nullable=True)
    user: "User" = Relationship(back_populates="jobs")


class JobRead(BaseModel):
    id: int
    title: str
    text: str
    location: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class JobCreate(BaseModel):
    title: str
    text: str
    location: str


class JobUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
