"""API schemas for error messages."""

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Schema for error message"""

    detail: str
