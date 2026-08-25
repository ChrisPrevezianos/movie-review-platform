import datetime
import uuid
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.links import MovieDirector

if TYPE_CHECKING:
    from app.models.movie import Movie

class Director(SQLModel, table=True):
    __tablename__ = "directors"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    last_name: str = Field(index=True, max_length=50)
    first_name: str = Field(index=True, max_length=50)
    birth_date: datetime.date | None = Field(default=None)
    movies: list["Movie"] = Relationship(back_populates="directors", link_model=MovieDirector)