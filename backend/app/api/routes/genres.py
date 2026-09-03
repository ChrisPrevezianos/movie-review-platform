"""API routes for Genre management and retrieval."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import SessionDep, get_current_active_superuser
from app.schemas.genre import GenrePublic, GenresPublic, GenreCreate, GenreUpdate
from app.services import genre_service

router = APIRouter(prefix="/genres", tags=["genres"])

@router.get("", response_model=GenresPublic)
def get_genres(*, session: SessionDep) -> GenresPublic:
    """Return all available genres with the total count."""
    genres = genre_service.get_genres(session=session)
    genres_public = [GenrePublic.model_validate(genre) for genre in genres]
    return GenresPublic(genres=genres_public, count=len(genres))

@router.get("/{genre_id}", response_model=GenrePublic)
def get_genre(*, session: SessionDep, genre_id: uuid.UUID) -> GenrePublic:
    """Return a genre by ID or raise 404 if it does not exist."""
    genre = genre_service.get_genre_by_id(session=session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre

@router.post("", response_model=GenrePublic, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_superuser)])
def create_genre(*, session: SessionDep, genre_in: GenreCreate) -> GenrePublic:
   """Create a new genre. Requires superuser privileges."""
   return genre_service.create_genre(session=session, genre_create=genre_in)

@router.patch("/{genre_id}", response_model=GenrePublic, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_superuser)])
def update_genre(*, session:SessionDep, genre_id: uuid.UUID, genre_in: GenreUpdate) -> GenrePublic:
    """Update an existing genre. Requires superuser privileges."""
    genre = genre_service.get_genre_by_id(session=session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre_service.update_genre(session=session, db_genre=genre, genre_update=genre_in)

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_superuser)])
def delete_genre(*, session: SessionDep, genre_id: uuid.UUID) -> None:
    """Delete a genre if it exists and is not associated with movies. Requires superuser privileges."""
    genre = genre_service.get_genre_by_id(session=session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    genre_service.delete_genre(session=session, db_genre=genre)