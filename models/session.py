from datetime import datetime
from typing import TYPE_CHECKING, Optional
from models.base import BaseModel, BaseTableFields
from sqlmodel import Field, Relationship, Column, String

if TYPE_CHECKING:
    from models.user import User


class Session(BaseModel, BaseTableFields, table=True):
    __tablename__ = "sessions"

    access_token: str = Field(
        sa_column=Column(
            String,
            unique=True,
            nullable=False
        )
    )
    ip_address: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True
        )
    )
    user_agent: Optional[str] = Field(
        sa_column=Column(
            String(100),
            nullable=True
        )
    )

    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="sessions")


class SessionRead(BaseModel):
    id: int
    access_token: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool


class SessionCreate(BaseModel):
    access_token: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    user_id: int


class SessionUpdate(BaseModel):
    is_active: Optional[bool] = None
