import uuid
from sqlmodel import Session, select
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate

def create_genre(*, session: Session, genre_create: GenreCreate) -> Genre:
    db_genre = Genre.model_validate(genre_create)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre

def get_genre_by_id(*, session: Session, genre_id: uuid.UUID) -> Genre | None:
    session_genre = session.get(Genre, genre_id)
    return session_genre

def get_genres(*, session: Session) -> list[Genre]:
    statement = select(Genre)
    session_genres = session.exec(statement).all()
    return list(session_genres)

def update_genre(*, session: Session, db_genre: Genre, genre_update: GenreUpdate) -> Genre:
    genre_data = genre_update.model_dump(exclude_unset=True)
    db_genre.sqlmodel_update(genre_data)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre

def delete_genre(*, session: Session, db_genre: Genre) -> None:
    session.delete(db_genre)
    session.commit()

def get_genre_by_name(*, session: Session, genre_name: str) -> Genre | None:
    """Return a genre by name using a case-insensitive search.
    Used to prevent duplicate genre names during create and update operations.
    """
    statement = select(Genre).where(Genre.name.ilike(genre_name))
    session_genre = session.exec(statement).first()
    return session_genre