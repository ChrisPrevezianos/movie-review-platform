import datetime
import uuid
from sqlmodel import Field, SQLModel

class ReviewCreate(SQLModel):
    rating: int = Field(ge=1, le=10)  # Rating between 1 and 10
    comment: str | None = Field(default=None)

class ReviewUpdate(SQLModel):
    rating: int | None = Field(default=None, ge=1, le=10)  # Rating between 1 and 10
    comment: str | None = Field(default=None)

class ReviewPublic(SQLModel):
    id: uuid.UUID
    rating: int
    comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    user_id: uuid.UUID
    movie_id: uuid.UUID

class ReviewsPublic(SQLModel):
    reviews: list[ReviewPublic]
    count: int