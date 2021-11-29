from sqlmodel import Field, SQLModel


class PermissionRoleLink(SQLModel, table=True):
    __tablename__ = "permission_role_link"

    permission_id: int = Field(
        foreign_key="permissions.id",
        primary_key=True,
    )

    role_id: int = Field(
        foreign_key="roles.id",
        primary_key=True,
    )
