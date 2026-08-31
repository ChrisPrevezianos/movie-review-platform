"""Service functions for Actor business rules and repository operations."""
import uuid
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.actor import Actor
from app.schemas.actor import ActorCreate, ActorUpdate
from app.repositories import actor_repository as actor_repo

def create_actor(*, session: Session, actor_create: ActorCreate) -> Actor:
    """Create an actor after normalizing names and preventing empty or duplicate values."""
    actor_create.first_name = actor_create.first_name.strip()
    if actor_create.first_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="First name cannot be empty."
        )
    actor_create.last_name = actor_create.last_name.strip()
    if actor_create.last_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Last name cannot be empty."
        )
    existing_actor = actor_repo.get_actor_by_name(session=session, actor_first_name=actor_create.first_name,actor_last_name=actor_create.last_name)
    if existing_actor is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Actor already exists."
        )
    return actor_repo.create_actor(session=session, actor_create=actor_create)

def get_actor_by_id(*, session: Session, actor_id: uuid.UUID) -> Actor | None:
    return actor_repo.get_actor_by_id(session=session, actor_id=actor_id)

def get_actors(*, session: Session, skip: int = 0, limit: int = 10) -> list[Actor]:
    """Return actors with pagination."""
    return actor_repo.get_actors(session=session, skip=skip, limit=limit)

def update_actor(*, session: Session, db_actor: Actor, actor_update:ActorUpdate) -> Actor:
    """Update an actor after normalizing names and preventing empty, unchanged, or duplicate data."""
    if actor_update.first_name is not None:
        actor_update.first_name = actor_update.first_name.strip()
        if actor_update.first_name == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="First name cannot be empty."
            )

    if actor_update.last_name is not None:
        actor_update.last_name = actor_update.last_name.strip()
        if actor_update.last_name == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Last name cannot be empty."
            )

    actor_data = actor_update.model_dump(exclude_unset=True)
    db_data = db_actor.model_dump(include=set(actor_data.keys()))

    if actor_data == db_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes to update."
        )

    search_first = actor_update.first_name if actor_update.first_name is not None else db_actor.first_name
    search_last = actor_update.last_name if actor_update.last_name is not None else db_actor.last_name

    if "first_name" in actor_data or "last_name" in actor_data:
        existing_actor = actor_repo.get_actor_by_name(session=session, actor_first_name=search_first,actor_last_name=search_last)
        if existing_actor and existing_actor.id != db_actor.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Actor already exists."
            )
    return actor_repo.update_actor(session=session, db_actor=db_actor, actor_update=actor_update)

def delete_actor(*, session: Session, db_actor: Actor) -> None:
    """Delete an actor only if they are not associated with any movies."""
    if db_actor.movies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Actor has associated movies."
        )
    return actor_repo.delete_actor(session=session, db_actor=db_actor)

def search_actors(*, session: Session, search_term: str, skip: int = 0, limit: int = 10) -> list[Actor]:
    """Search actors by first name, last name, or full name with pagination."""
    return actor_repo.search_actors(session=session, search_term=search_term, skip=skip, limit=limit)

def count_actors(*, session: Session) -> int:
    """Return the total number of actors."""
    return actor_repo.count_actors(session=session)

def count_actors_by_search(*, session: Session, search_term: str) -> int:
    """Return the total number of actors matching the search term."""
    return actor_repo.count_actors_by_search(session=session, search_term=search_term)