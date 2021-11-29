from typing import Optional
from sqlmodel import SQLModel, Field, func, DateTime, Column, Boolean
from datetime import datetime


class BaseModel(SQLModel):
    """
    BaseModel class
    """

    class Config:
        use_enum_values = True


class BaseTableFields(SQLModel):
    """
    BaseTableField class
    """

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )

    is_active: Optional[bool] = Field(
        default=None,
        sa_column=Column(Boolean, server_default='true', default=True)
    )
