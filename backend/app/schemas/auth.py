"""Authentication schemas for access tokens and JWT payloads."""
from sqlmodel import SQLModel

class Token(SQLModel):
    """Schema for the access token returned after successful authentication."""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    """Schema for the decoded JWT payload used to identify the authenticated user."""
    sub: str | None = None