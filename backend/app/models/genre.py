import uuid
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.links import MovieGenre

if TYPE_CHECKING:
    from app.models.movie import Movie

class Genre(SQLModel, table=True):
    __tablename__ = "genres"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)
    movies: list["Movie"] = Relationship(back_populates="genres", link_model=MovieGenre)