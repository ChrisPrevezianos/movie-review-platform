import uuid
from sqlmodel import Session, select
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

def get_actors(*, session: Session) -> list[Actor]:
    statement = select(Actor)
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