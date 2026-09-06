"""Schemas for Movie creation, updates, and public API responses."""
import datetime
from typing import Literal
import uuid
from sqlmodel import Field, SQLModel
from pydantic import HttpUrl
from app.schemas.actor import ActorCreate
from app.schemas.director import DirectorCreate
from app.schemas.genre import GenrePublic

AgeRating = Literal["G", "PG", "PG-13", "R", "NC-17"] 

class MovieCreate(SQLModel):
    """Schema for creating a movie with its genres, actors, and directors."""
    title: str = Field(max_length=100)
    synopsis: str = Field(min_length=50, max_length=1000)
    release_year: int = Field(ge=1888, le=datetime.datetime.now().year+1)  # Allow films released from 1888 through next year
    duration: int = Field(ge=1)  # Duration is stored in minutes
    age_rating: AgeRating
    poster_url: HttpUrl = Field(max_length=255)
    trailer_url: HttpUrl = Field(max_length=255)
    genre_ids: list[uuid.UUID] = Field(min_length=1) # IDs of predefined genres
    actors: list[ActorCreate] = Field(min_length=1) # At least one actor is required
    directors: list[DirectorCreate] = Field(min_length=1) # At least one director is required

class MovieUpdate(SQLModel):
    """Schema for partially updating a movie and its relationships."""
    title: str | None = Field(default=None, max_length=100)
    synopsis: str | None = Field(default=None, min_length=50, max_length=1000)
    release_year: int | None = Field(default=None, ge=1888, le=datetime.datetime.now().year+1)  # Allow films released from 1888 through next year
    duration: int | None = Field(default=None, ge=1)  # Duration is stored in minutes
    age_rating: AgeRating | None = Field(default=None)
    poster_url: HttpUrl | None = Field(default=None, max_length=255)
    trailer_url: HttpUrl | None = Field(default=None, max_length=255)
    genre_ids: list[uuid.UUID] | None = Field(default=None, min_length=1) # Optional genre relationship update
    actors: list[ActorCreate] | None = Field(default=None, min_length=1) # Optional actor relationship update
    directors: list[DirectorCreate] | None = Field(default=None, min_length=1) # Optional director relationship update

class PersonSummary(SQLModel):
    """Compact actor or director representation used inside movie responses."""
    id: uuid.UUID
    first_name: str
    last_name: str

class MoviePublic(SQLModel):
    """Public representation of a movie with its related genres, actors, and directors."""
    id: uuid.UUID
    title: str
    synopsis: str
    release_year: int
    duration: int
    age_rating: AgeRating
    poster_url: HttpUrl
    trailer_url: HttpUrl
    created_at: datetime.datetime
    genres: list[GenrePublic]
    actors: list[PersonSummary]
    directors: list[PersonSummary]

class MoviesPublic(SQLModel):
    """Response schema for a collection of movies with the total count."""
    movies: list[MoviePublic]
    count: int

class MovieWithRatingPublic(MoviePublic):
    """Public movie representation including its average review rating."""
    average_rating: float

class MoviesWithRatingPublic(SQLModel):
    """Response schema for rated movies with the total count."""
    movies: list[MovieWithRatingPublic]
    count: int
