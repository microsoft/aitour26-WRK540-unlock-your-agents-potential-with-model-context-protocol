"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel


class RlsUserRequest(BaseModel):
    """Request model for setting RLS user."""

    id: str
    name: str


class RlsUserResult(BaseModel):
    """Response model for RLS user operations."""

    message: str
    rls_user_id: str
