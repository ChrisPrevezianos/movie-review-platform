"""API routes for Actor management, retrieval, search, and pagination."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import SessionDep, get_current_active_superuser
from app.schemas.actor import ActorPublic, ActorsPublic, ActorCreate, ActorUpdate
from app.services import actor_service

router = APIRouter(prefix="/actors", tags=["actors"])

@router.get("", response_model=ActorsPublic)
def get_actors(*, session: SessionDep, page: int = 1, page_size: int = 10, search: str | None = None) -> ActorsPublic:
    """Return actors with pagination and optional name search."""
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
        actors = actor_service.get_actors(session=session, skip=skip, limit=page_size)
        total_count = actor_service.count_actors(session=session)
    else:
        actors = actor_service.search_actors(session=session, search_term=search, skip=skip, limit=page_size)
        total_count = actor_service.count_actors_by_search(session=session, search_term=search)
    actors_public = [ActorPublic.model_validate(actor) for actor in actors]
    return ActorsPublic(actors=actors_public, count=total_count)
    
@router.get("/{actor_id}", response_model=ActorPublic)
def get_actor(*, session: SessionDep, actor_id: uuid.UUID) -> ActorPublic:
    """Return an actor by ID or raise 404 if they do not exist."""
    actor = actor_service.get_actor_by_id(session=session, actor_id=actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actor not found"
        )
    return actor

@router.post("", response_model=ActorPublic, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_superuser)])
def create_actor(*, session: SessionDep, actor_in: ActorCreate) -> ActorPublic:
    """Create a new actor. Requires superuser privileges."""
    return actor_service.create_actor(session=session, actor_create=actor_in)

@router.patch("/{actor_id}", response_model=ActorPublic, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_superuser)])
def update_actor(*, session:SessionDep, actor_id: uuid.UUID, actor_in: ActorUpdate) -> ActorPublic:
    """Update an existing actor. Requires superuser privileges."""
    actor = actor_service.get_actor_by_id(session=session, actor_id=actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actor not found"
        )
    return actor_service.update_actor(session=session, db_actor=actor, actor_update=actor_in)

@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_superuser)])
def delete_actor(*, session: SessionDep, actor_id: uuid.UUID) -> None:
    """Delete an actor if they exist and are not associated with movies. Requires superuser privileges."""
    actor = actor_service.get_actor_by_id(session=session, actor_id=actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actor not found"
        )
    actor_service.delete_actor(session=session, db_actor=actor)
