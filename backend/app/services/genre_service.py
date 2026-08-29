import uuid
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate
from app.repositories import genre_repository as genre_repo

def create_genre(*, session: Session, genre_create: GenreCreate) -> Genre:
    """Create a genre after normalizing its name and preventing duplicates."""
    genre_create.name = genre_create.name.strip()
    if genre_create.name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre name cannot be empty."
        )
    existing_genre = genre_repo.get_genre_by_name(session=session, genre_name=genre_create.name)
    if existing_genre is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre already exists."
        )
    return genre_repo.create_genre(session=session, genre_create=genre_create)

def get_genre_by_id(*, session: Session, genre_id: uuid.UUID) -> Genre | None:
    return genre_repo.get_genre_by_id(session=session, genre_id=genre_id)

def get_genres(*, session: Session) -> list[Genre]:
    return genre_repo.get_genres(session=session)

def update_genre(*, session: Session, db_genre: Genre, genre_update:GenreUpdate) -> Genre:
    """Update a genre after normalizing its name and preventing duplicates."""
    genre_update.name = genre_update.name.strip()
    if genre_update.name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre name cannot be empty."
        )
    existing_genre = genre_repo.get_genre_by_name(session=session, genre_name=genre_update.name)
    if existing_genre is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre already exists."
        )
    return genre_repo.update_genre(session=session, db_genre=db_genre, genre_update=genre_update)

def delete_genre(*, session: Session, db_genre: Genre) -> None:
    """Delete a genre only if it is not associated with any movies."""
    if db_genre.movies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre has associated movies."
        )
    return genre_repo.delete_genre(session=session, db_genre=db_genre)