from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from models.base import BaseModel, BaseTableFields
from sqlmodel import Field, Relationship, Column, String
from models.permission_role import PermissionRoleLink

if TYPE_CHECKING:
    from models.role import Role


class Permission(BaseModel, BaseTableFields, table=True):
    __tablename__ = "permissions"

    name: str = Field(
        sa_column=Column(
            String(50),
            unique=True,
            nullable=False
        )
    )

    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=PermissionRoleLink
    )


class PermissionRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


class PermissionCreate(BaseModel):
    name: str


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
