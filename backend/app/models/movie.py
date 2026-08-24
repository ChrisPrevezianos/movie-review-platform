import datetime 
from sqlalchemy import DateTime
import uuid
from sqlmodel import Field, SQLModel

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