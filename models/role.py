from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from models.base import BaseModel, BaseTableFields
from sqlmodel import Field, Relationship, Column, String
from models.permission_role import PermissionRoleLink

if TYPE_CHECKING:
    from models.permission import Permission
    from models.user import User


class Role(BaseModel, BaseTableFields, table=True):
    __tablename__ = "roles"

    name: str = Field(
        sa_column=Column(
            String(50),
            unique=True,
            nullable=False
        )
    )

    users: List["User"] = Relationship(back_populates="role")
    permissions: List["Permission"] = Relationship(
        back_populates="roles",
        link_model=PermissionRoleLink
    )


class RoleRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
