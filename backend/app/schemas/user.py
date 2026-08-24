import datetime
import uuid
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserCreate(SQLModel):
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)

# Admin-only user update schema
class UserUpdate(SQLModel):
    username: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None
    is_superuser: bool | None = None

class UserUpdateMe(SQLModel):
    username: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

# Public user data exposed to other users
class UserPublic(SQLModel):
    id: uuid.UUID
    username: str
    created_at: datetime.datetime

class UsersPublic(SQLModel):
    users: list[UserPublic]
    count: int