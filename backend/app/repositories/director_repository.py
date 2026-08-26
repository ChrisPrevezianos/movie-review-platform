import uuid
from sqlmodel import Session, select
from app.models.director import Director
from app.schemas.director import DirectorCreate, DirectorUpdate

def create_director(*, session: Session, director_create: DirectorCreate) -> Director:
    db_director = Director.model_validate(director_create)
    session.add(db_director)
    session.commit()
    session.refresh(db_director)
    return db_director

def get_director_by_id(*, session: Session, director_id: uuid.UUID) -> Director | None:
    session_director = session.get(Director, director_id)
    return session_director

def get_directors(*, session: Session) -> list[Director]:
    statement = select(Director)
    session_directors = session.exec(statement).all()
    return list(session_directors)

def update_director(*, session: Session, db_director: Director, director_update: DirectorUpdate) -> Director:
    director_data = director_update.model_dump(exclude_unset=True)
    db_director.sqlmodel_update(director_data)
    session.add(db_director)
    session.commit()
    session.refresh(db_director)
    return db_director

def delete_director(*, session: Session, db_director: Director) -> None:
    session.delete(db_director)
    session.commit()