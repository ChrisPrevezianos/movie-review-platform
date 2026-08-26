import uuid
from sqlmodel import Session, select
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.actor import Actor
from app.models.director import Director
from app.models.review import Review
from app.schemas.movie import MovieCreate, MovieUpdate
from sqlalchemy import func

def create_movie(*, session: Session, movie_create: MovieCreate) -> Movie:
    db_movie = Movie.model_validate(movie_create)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def get_movie_by_id(*, session: Session, movie_id: uuid.UUID) -> Movie | None:
    session_movie = session.get(Movie, movie_id)
    return session_movie

def get_movies(*, session: Session) -> list[Movie]:
    statement = select(Movie)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def update_movie(*, session: Session, db_movie: Movie, movie_update: MovieUpdate) -> Movie:
    movie_data = movie_update.model_dump(exclude_unset=True)
    db_movie.sqlmodel_update(movie_data)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def delete_movie(*, session: Session, db_movie: Movie) -> None:
    session.delete(db_movie)
    session.commit()

def get_movies_by_title(*, session: Session, title: str) -> list[Movie]:
    search_pattern = f"%{title}%"
    statement = select(Movie).where(Movie.title.ilike(search_pattern))
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_release_year(*, session: Session, release_year: int) -> list[Movie]:
    statement = select(Movie).where(Movie.release_year == release_year)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_age_rating(*, session: Session, age_rating: str) -> list[Movie]:
    statement = select(Movie).where(Movie.age_rating == age_rating)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_genre(*, session: Session, genre: str) -> list[Movie]:
    statement = select(Movie).join(Movie.genres).where(Genre.name == genre)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_actor(*, session: Session, actor_name: str) -> list[Movie]:
    search_pattern = f"%{actor_name}%"
    statement = select(Movie).join(Movie.actors).where(Actor.last_name.ilike(search_pattern) | Actor.first_name.ilike(search_pattern))
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_director(*, session: Session, director_name: str) -> list[Movie]:
    search_pattern = f"%{director_name}%"
    statement = select(Movie).join(Movie.directors).where(Director.last_name.ilike(search_pattern) | Director.first_name.ilike(search_pattern))
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_min_rating(*, session: Session, min_rating: float) -> list[Movie]:
    statement = select(Movie).join(Movie.reviews).group_by(Movie.id).having(func.avg(Review.rating) >= min_rating)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_ordered_by_rating(*, session: Session) -> list[Movie]:
    statement = select(Movie).join(Movie.reviews).group_by(Movie.id).order_by(func.avg(Review.rating).desc())
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_top_rated_movies(*, session: Session, limit: int = 10) -> list[Movie]:
    statement = select(Movie).join(Movie.reviews).group_by(Movie.id).order_by(func.avg(Review.rating).desc()).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)