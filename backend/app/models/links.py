import uuid
from sqlmodel import Field, SQLModel


class MovieActor(SQLModel, table=True):
    """Association table for the many-to-many relationship between movies and actors."""
    __tablename__ = "movie_actors"
    movie_id: uuid.UUID = Field(foreign_key="movies.id", primary_key=True)
    actor_id: uuid.UUID = Field(foreign_key="actors.id", primary_key=True)

class MovieDirector(SQLModel, table=True):
    """Association table for the many-to-many relationship between movies and directors."""
    __tablename__ = "movie_directors"
    movie_id: uuid.UUID = Field(foreign_key="movies.id", primary_key=True)
    director_id: uuid.UUID = Field(foreign_key="directors.id", primary_key=True)

class MovieGenre(SQLModel, table=True):
    """Association table for the many-to-many relationship between movies and genres."""
    __tablename__ = "movie_genres"
    movie_id: uuid.UUID = Field(foreign_key="movies.id", primary_key=True)
    genre_id: uuid.UUID = Field(foreign_key="genres.id", primary_key=True)