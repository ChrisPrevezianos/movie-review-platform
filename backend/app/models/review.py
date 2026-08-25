import datetime
import uuid
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import DateTime, UniqueConstraint

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.user import User

def get_datetime_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="uq_review_user_movie"),
    )
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    rating: int = Field(index=True, ge=1, le=10)  # Rating between 1 and 10
    comment: str | None = Field(default=None)
    created_at: datetime.datetime = Field(
            index=True, 
            default_factory=get_datetime_utc, 
            sa_type=DateTime(timezone=True),  # type: ignore
        )
    updated_at: datetime.datetime | None = Field(
            index=True,
            default=None,
            sa_type=DateTime(timezone=True),  # type: ignore
        )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    movie_id: uuid.UUID = Field(foreign_key="movies.id", index=True)
    movie: "Movie" = Relationship(back_populates="reviews")
    user: "User" = Relationship(back_populates="reviews")