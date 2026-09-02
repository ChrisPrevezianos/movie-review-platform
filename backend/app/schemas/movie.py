"""Schemas for Movie creation, updates, and public API responses."""
import datetime
from typing import Literal
import uuid
from sqlmodel import Field, SQLModel
from pydantic import HttpUrl

AgeRating = Literal["G", "PG", "PG-13", "R", "NC-17"] 

class MovieCreate(SQLModel):
    """Schema for creating a movie, including its selected genres."""
    title: str = Field(max_length=100)
    synopsis: str = Field(min_length=50, max_length=1000)
    release_year: int = Field(ge=1888, le=datetime.datetime.now().year+1)  # Allow films released from 1888 through next year
    duration: int = Field(ge=1)  # Duration is stored in minutes
    age_rating: AgeRating
    poster_url: HttpUrl = Field(max_length=255)
    trailer_url: HttpUrl = Field(max_length=255)
    genre_ids: list[uuid.UUID] = Field(min_length=1) # IDs of predefined genres

class MovieUpdate(SQLModel):
    """Schema for partially updating a movie and optionally its genres."""
    title: str | None = Field(default=None, max_length=100)
    synopsis: str | None = Field(default=None, min_length=50, max_length=1000)
    release_year: int | None = Field(default=None, ge=1888, le=datetime.datetime.now().year+1)  # Allow films released from 1888 through next year
    duration: int | None = Field(default=None, ge=1)  # Duration is stored in minutes
    age_rating: AgeRating | None = Field(default=None)
    poster_url: HttpUrl | None = Field(default=None, max_length=255)
    trailer_url: HttpUrl | None = Field(default=None, max_length=255)
    genre_ids: list[uuid.UUID] | None = Field(default=None, min_length=1) # Optional genre relationship update

class MoviePublic(SQLModel):
    """Public representation of a movie."""
    id: uuid.UUID
    title: str
    synopsis: str
    release_year: int
    duration: int
    age_rating: AgeRating
    poster_url: HttpUrl
    trailer_url: HttpUrl
    created_at: datetime.datetime

class MoviesPublic(SQLModel):
    """Response schema for a collection of movies with the total count."""
    movies: list[MoviePublic]
    count: int