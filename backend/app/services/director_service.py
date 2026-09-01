"""Service functions for Director business rules and repository operations."""
import uuid
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.director import Director
from app.schemas.director import DirectorCreate, DirectorUpdate
from app.repositories import director_repository as director_repo

def create_director(*, session: Session, director_create: DirectorCreate) -> Director:
    """Create a director after normalizing names and preventing empty or duplicate values."""
    director_create.first_name = director_create.first_name.strip()
    if director_create.first_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First name cannot be empty"
        )
    director_create.last_name = director_create.last_name.strip()
    if director_create.last_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last name cannot be empty"
        )
    existing_director = director_repo.get_director_by_name(session=session, director_first_name=director_create.first_name, director_last_name=director_create.last_name)
    if existing_director is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Director already exists"
        )
    return director_repo.create_director(session=session, director_create=director_create)

def get_director_by_id(*, session: Session, director_id: uuid.UUID) -> Director | None:
    return director_repo.get_director_by_id(session=session, director_id=director_id)

def get_directors(*, session: Session, skip: int = 0, limit: int = 10) -> list[Director]:
    """Return directors with pagination."""
    return director_repo.get_directors(session=session, skip=skip, limit=limit)

def update_director(*, session: Session, db_director: Director, director_update: DirectorUpdate) -> Director:
    """Update a director after normalizing names and preventing empty, unchanged, or duplicate data."""
    if director_update.first_name is not None:
        director_update.first_name = director_update.first_name.strip()
        if director_update.first_name == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="First name cannot be empty"
            )
        
    if director_update.last_name is not None:
        director_update.last_name = director_update.last_name.strip()
        if director_update.last_name == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Last name cannot be empty"
            )

    director_data = director_update.model_dump(exclude_unset=True)
    db_data = db_director.model_dump(include=set(director_data.keys()))

    if director_data == db_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes to update"
        )

    search_first = director_update.first_name if director_update.first_name is not None else db_director.first_name
    search_last = director_update.last_name if director_update.last_name is not None else db_director.last_name

    if "first_name" in director_data or "last_name" in director_data:
        existing_director = director_repo.get_director_by_name(session=session, director_first_name=search_first, director_last_name=search_last)
        if existing_director and existing_director.id != db_director.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Director already exists"
            )
    return director_repo.update_director(session=session, db_director=db_director, director_update=director_update)

def delete_director(*, session: Session, db_director: Director) -> None:
    """Delete a director only if they are not associated with any movies."""
    if db_director.movies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Director is associated with movies"
        )
    return director_repo.delete_director(session=session, db_director=db_director)

def search_directors(*, session: Session, search_term: str, skip: int = 0, limit: int = 10) -> list[Director]:
    """Search directors by first name, last name, or full name with pagination."""
    return director_repo.search_directors(session=session, search_term=search_term, skip=skip, limit=limit)

def count_directors(*, session: Session) -> int:
    """Return the total number of directors."""
    return director_repo.count_directors(session=session)

def count_directors_by_search(*, session: Session, search_term: str) -> int:
    """Return the total number of directors matching the search term."""
    return director_repo.count_directors_by_search(session=session, search_term=search_term)