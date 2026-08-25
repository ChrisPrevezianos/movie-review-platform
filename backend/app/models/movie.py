import datetime 
import uuid
from sqlalchemy import DateTime
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.links import MovieActor, MovieDirector, MovieGenre

if TYPE_CHECKING:
    from app.models.actor import Actor
    from app.models.director import Director
    from app.models.genre import Genre
    from app.models.review import Review

def get_datetime_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class Movie(SQLModel, table=True):
    __tablename__ = "movies"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True, max_length=100)
    synopsis: str = Field(min_length=50, max_length=1000)
    release_year: int = Field(index=True, ge=1888)  # The first film was made in 1888
    duration: int = Field(index=True, ge=1)  # Minimum duration of 1 minute
    age_rating: str = Field(index=True)
    poster_url: str = Field(max_length=255)
    trailer_url: str = Field(max_length=255)
    created_at: datetime.datetime = Field(
        index=True, 
        default_factory=get_datetime_utc, 
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    actors: list["Actor"] = Relationship(back_populates="movies", link_model=MovieActor)
    directors: list["Director"] = Relationship(back_populates="movies", link_model=MovieDirector)
    genres: list["Genre"] = Relationship(back_populates="movies", link_model=MovieGenre)
    reviews: list["Review"] = Relationship(back_populates="movie", cascade_delete=True)