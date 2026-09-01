"""API routes for Director management, retrieval, search, and pagination."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import SessionDep, get_current_active_superuser
from app.schemas import DirectorPublic, DirectorsPublic, DirectorCreate, DirectorUpdate
from app.services import director_service

router = APIRouter(prefix="/directors", tags=["directors"])

@router.get("", response_model=DirectorsPublic)
def get_directors(*, session: SessionDep, page: int = 1, page_size: int = 10, search: str | None = None) -> DirectorsPublic:
    """Return directors with pagination and optional name search."""
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be greater than or equal to 1"
        )
    if page_size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be greater than or equal to 1"
        )
    if page_size > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size cannot be greater than 50"
        )
    if search is not None:
        search = search.strip()
        if search == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search term cannot be empty"
            )

    skip = (page - 1) * page_size
    if search is None:
        directors = director_service.get_directors(session=session, skip=skip, limit=page_size)
        total_count = director_service.count_directors(session=session)
    else:
        directors = director_service.search_directors(session=session, search_term=search, skip=skip, limit=page_size)
        total_count = director_service.count_directors_by_search(session=session, search_term=search)
    directors_public = [DirectorPublic.model_validate(director) for director in directors]
    return DirectorsPublic(directors=directors_public, count=total_count)

@router.get("/{director_id}", response_model=DirectorPublic)
def get_director(*, session: SessionDep, director_id: uuid.UUID) -> DirectorPublic:
    """Return a director by ID or raise 404 if they do not exist."""
    director = director_service.get_director_by_id(session=session, director_id=director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director not found"
        )
    return director

@router.post("", response_model=DirectorPublic, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_superuser)])
def create_director(*, session: SessionDep, director_in: DirectorCreate) -> DirectorPublic:
    """Create a new director. Requires superuser privileges."""
    return director_service.create_director(session=session, director_create=director_in)

@router.patch("/{director_id}", response_model=DirectorPublic, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_superuser)])
def update_director(*, session:SessionDep, director_id: uuid.UUID, director_in: DirectorUpdate) -> DirectorPublic:
    """Update an existing director. Requires superuser privileges."""
    director = director_service.get_director_by_id(session=session, director_id=director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director not found"
        )
    return director_service.update_director(session=session, db_director=director, director_update=director_in)

@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_superuser)])
def delete_director(*, session: SessionDep, director_id: uuid.UUID) -> None:
    """Delete a director if they exist and are not associated with movies. Requires superuser privileges."""
    director = director_service.get_director_by_id(session=session, director_id=director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Director not found"
        )
    director_service.delete_director(session=session, db_director=director)