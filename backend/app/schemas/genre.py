import uuid
from sqlmodel import Field, SQLModel


class GenreCreate(SQLModel):
    name: str = Field(max_length=100)

class GenreUpdate(SQLModel):
    name: str = Field(max_length=100)

class GenrePublic(SQLModel):
    id: uuid.UUID
    name: str

class GenresPublic(SQLModel):
    genres: list[GenrePublic]
    count: int