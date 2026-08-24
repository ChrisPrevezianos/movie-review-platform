import datetime
import uuid
from sqlmodel import Field, SQLModel

class DirectorCreate(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    birth_date: datetime.date | None = Field(default=None) 

class DirectorUpdate(SQLModel):
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    birth_date: datetime.date | None = Field(default=None)

class DirectorPublic(SQLModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    birth_date: datetime.date | None

class DirectorsPublic(SQLModel):
    directors: list[DirectorPublic]
    count: int