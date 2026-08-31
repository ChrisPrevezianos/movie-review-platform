"""Repository functions for Actor database operations, search, and pagination."""
import uuid
from sqlmodel import Session, select, func
from app.models.actor import Actor
from app.schemas.actor import ActorCreate, ActorUpdate

def create_actor(*, session: Session, actor_create: ActorCreate) -> Actor:
    db_actor = Actor.model_validate(actor_create)
    session.add(db_actor)
    session.commit()
    session.refresh(db_actor)
    return db_actor

def get_actor_by_id(*, session: Session, actor_id: uuid.UUID) -> Actor | None:
    session_actor = session.get(Actor, actor_id)
    return session_actor

def get_actors(*, session: Session, skip: int = 0, limit: int = 10) -> list[Actor]:
    """Return actors with pagination, ordered by last name, first name, and ID."""
    statement = select(Actor).offset(skip).limit(limit).order_by(Actor.last_name.asc(), Actor.first_name.asc(), Actor.id.asc())
    session_actors = session.exec(statement).all()
    return list(session_actors)

def update_actor(*, session: Session, db_actor: Actor, actor_update: ActorUpdate) -> Actor:
    actor_data = actor_update.model_dump(exclude_unset=True)
    db_actor.sqlmodel_update(actor_data)
    session.add(db_actor)
    session.commit()
    session.refresh(db_actor)
    return db_actor

def delete_actor(*, session: Session, db_actor: Actor) -> None:
    session.delete(db_actor)
    session.commit()

def get_actor_by_name(*, session: Session, actor_first_name: str, actor_last_name: str) -> Actor | None:
    """Return an actor by first and last name using a case-insensitive search.
    Used to prevent duplicate actors during create and update operations.
    """
    statement = select(Actor).where(Actor.first_name.ilike(actor_first_name),Actor.last_name.ilike(actor_last_name)) 
    session_actor = session.exec(statement).first()
    return session_actor

def search_actors(*, session: Session, search_term: str, skip: int = 0, limit: int = 10) -> list[Actor]:
    """Search actors by first name, last name, or full name with pagination."""
    search_pattern = f"%{search_term}%"
    statement = select(Actor).where(Actor.first_name.ilike(search_pattern) | Actor.last_name.ilike(search_pattern) | func.concat(Actor.first_name, " ", Actor.last_name).ilike(search_pattern)).order_by(Actor.last_name.asc(), Actor.first_name.asc(), Actor.id.asc()).offset(skip).limit(limit)
    session_actors = session.exec(statement).all()
    return list(session_actors)

def count_actors(*, session: Session) -> int:
    """Return the total number of actors."""
    statement = select(func.count()).select_from(Actor)
    total_count = session.exec(statement).one()
    return total_count

def count_actors_by_search(*, session: Session, search_term: str) -> int:
    """Return the total number of actors matching the search term."""
    search_pattern = f"%{search_term}%"
    statement = select(func.count()).select_from(Actor).where(Actor.first_name.ilike(search_pattern) | Actor.last_name.ilike(search_pattern) | func.concat(Actor.first_name, " ", Actor.last_name).ilike(search_pattern))
    total_count = session.exec(statement).one()
    return total_count