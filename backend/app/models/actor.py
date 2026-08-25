import datetime
import uuid
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.links import MovieActor

if TYPE_CHECKING:
    from app.models.movie import Movie

class Actor(SQLModel, table=True):
    __tablename__ = "actors"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(index=True, max_length=50)
    last_name: str = Field(index=True, max_length=50)
    birth_date: datetime.date | None = Field(default=None) 
    movies: list["Movie"] = Relationship(back_populates="actors", link_model=MovieActor)