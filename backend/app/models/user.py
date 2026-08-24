import datetime
import uuid
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

def get_datetime_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime.datetime = Field(
            index=True, 
            default_factory=get_datetime_utc, 
            sa_type=DateTime(timezone=True),  # type: ignore
        )