"""Schemas for User creation, updates, account management, and API responses."""
import datetime
import uuid
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserCreate(SQLModel):
    """Schema for public user registration."""
    username: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(SQLModel):
    """Schema for admin-only user account updates."""
    username: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None
    is_superuser: bool | None = None

class UserUpdateMe(SQLModel):
    """Schema for updating the current user's profile."""
    username: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)


class UpdatePassword(SQLModel):
    """Schema for changing the current user's password."""
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

class UserPublic(SQLModel):
    """Public user data that may be exposed to other users."""
    id: uuid.UUID
    username: str
    created_at: datetime.datetime

class UsersPublic(SQLModel):
    """Response schema for a public user collection with the total count."""
    users: list[UserPublic]
    count: int

class UserOwnData(SQLModel):
    """Profile data available to the currently authenticated user."""
    id: uuid.UUID
    username: str
    email: EmailStr
    created_at: datetime.datetime

class UserPrivateData(SQLModel):
    """Private user account data available to administrators."""
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime.datetime

class UsersPrivateData(SQLModel):
    """Response schema for an admin user collection with the total count."""
    users: list[UserPrivateData]
    count: int