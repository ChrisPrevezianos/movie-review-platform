"""Repository functions for Movie database operations, filtering, ratings, and pagination."""
import uuid
from sqlmodel import Session, select
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.actor import Actor
from app.models.director import Director
from app.models.review import Review
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieUpdate
from sqlalchemy import func

def create_movie(*, session: Session, genres: list[Genre], movie_create: MovieCreate) -> Movie:
    """Create and persist a movie with its selected genre relationships."""
    movie_data = movie_create.model_dump(exclude={"genre_ids"})
    db_movie = Movie.model_validate(movie_data)
    db_movie.genres = genres
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def get_movie_by_id(*, session: Session, movie_id: uuid.UUID) -> Movie | None:
    """Return a movie by ID, if it exists."""
    session_movie = session.get(Movie, movie_id)
    return session_movie

def get_movies(*, session: Session, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies with pagination, ordered by newest release year first."""
    statement = select(Movie).order_by(Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def update_movie(*, session: Session, db_movie: Movie, genres: list[Genre] | None, movie_update: MovieUpdate) -> Movie:
    """Update movie fields and optionally replace its genre relationships."""
    movie_data = movie_update.model_dump(exclude_unset=True, exclude={"genre_ids"})
    db_movie.sqlmodel_update(movie_data)
    if genres is not None:
        db_movie.genres = genres
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def delete_movie(*, session: Session, db_movie: Movie) -> None:
    """Delete a movie from the database."""
    session.delete(db_movie)
    session.commit()

def get_movie_by_exact_title(*, session: Session, title: str) -> list[Movie]:
    """Return movies whose title exactly matches the given title.
    Used by the service to enforce the title + release year duplicate rule.
    """
    statement = select(Movie).where(Movie.title == title)
    session_movie = session.exec(statement).all()
    return list(session_movie)

def get_movies_by_title(*, session: Session, title: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Search movies by partial, case-insensitive title with pagination.
    Results are ordered by newest release year first.
    """
    search_pattern = f"%{title}%"
    statement = select(Movie).where(Movie.title.ilike(search_pattern)).order_by(Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_release_year(*, session: Session, release_year: int, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies from a specific release year with pagination, ordered alphabetically by title."""
    statement = select(Movie).where(Movie.release_year == release_year).order_by(Movie.title.asc(), Movie.id.asc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_age_rating(*, session: Session, age_rating: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies with the given age rating with pagination, ordered by newest release year first."""
    statement = select(Movie).where(Movie.age_rating == age_rating).order_by(Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_genre(*, session: Session, genre: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies in the given genre with pagination, ordered by newest release year first."""
    statement = select(Movie).join(Movie.genres).where(Genre.name == genre).order_by(Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_actor(*, session: Session, actor_name: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies matching an actor's first name, last name, or full name with pagination.
    Results are ordered by newest release year first.
    """
    search_pattern = f"%{actor_name}%"
    statement = select(Movie).join(Movie.actors).where(Actor.last_name.ilike(search_pattern) | Actor.first_name.ilike(search_pattern) | func.concat(Actor.first_name, " ", Actor.last_name).ilike(search_pattern)).distinct().order_by(Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_director(*, session: Session, director_name: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies matching a director's first name, last name, or full name with pagination.
    Results are ordered by newest release year first.
    """
    search_pattern = f"%{director_name}%"
    statement = select(Movie).join(Movie.directors).where(Director.last_name.ilike(search_pattern) | Director.first_name.ilike(search_pattern) | func.concat(Director.first_name, " ", Director.last_name).ilike(search_pattern)).distinct().order_by(Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_by_min_rating(*, session: Session, min_rating: float, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies whose average rating from active users meets the minimum rating.
    Results are paginated and ordered by highest average rating first.
    """
    statement = select(Movie).join(Movie.reviews).join(User, Review.user_id == User.id).where(User.is_active == True).group_by(Movie.id).having(func.avg(Review.rating) >= min_rating).order_by(func.avg(Review.rating).desc(), Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_movies_ordered_by_rating(*, session: Session, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return reviewed movies ordered by average rating from active users, with pagination."""
    statement = select(Movie).join(Movie.reviews).join(User, Review.user_id == User.id).where(User.is_active == True).group_by(Movie.id).order_by(func.avg(Review.rating).desc(), Movie.release_year.desc(), Movie.id.desc()).offset(skip).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def get_top_rated_movies(*, session: Session, limit: int = 10) -> list[Movie]:
    """Return the highest-rated movies using reviews from active users, up to the given limit."""
    statement = select(Movie).join(Movie.reviews).join(User, Review.user_id == User.id).where(User.is_active == True).group_by(Movie.id).order_by(func.avg(Review.rating).desc(), Movie.release_year.desc(), Movie.id.desc()).limit(limit)
    session_movies = session.exec(statement).all()
    return list(session_movies)

def count_movies(*, session: Session) -> int:
    """Return the total number of movies."""
    statement = select(func.count()).select_from(Movie)
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_title(*, session: Session, title: str) -> int:
    """Return the total number of movies matching the partial title search."""
    search_pattern = f"%{title}%"
    statement = select(func.count()).select_from(Movie).where(Movie.title.ilike(search_pattern))
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_release_year(*, session: Session, release_year: int) -> int:
    """Return the total number of movies from the given release year."""
    statement = select(func.count()).select_from(Movie).where(Movie.release_year == release_year)
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_age_rating(*, session: Session, age_rating: str) -> int:
    """Return the total number of movies with the given age rating."""
    statement = select(func.count()).select_from(Movie).where(Movie.age_rating == age_rating)
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_genre(*, session: Session, genre: str) -> int:
    """Return the total number of movies in the given genre."""
    statement = select(func.count()).select_from(Movie).join(Movie.genres).where(Genre.name == genre)
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_actor(*, session: Session, actor_name: str) -> int:
    """Return the total number of distinct movies matching the actor name search."""
    search_pattern = f"%{actor_name}%"
    statement = select(func.count(func.distinct(Movie.id))).select_from(Movie).join(Movie.actors).where(Actor.last_name.ilike(search_pattern) | Actor.first_name.ilike(search_pattern) | func.concat(Actor.first_name, " ", Actor.last_name).ilike(search_pattern))
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_director(*, session: Session, director_name: str) -> int:
    """Return the total number of distinct movies matching the director name search."""
    search_pattern = f"%{director_name}%"
    statement = select(func.count(func.distinct(Movie.id))).select_from(Movie).join(Movie.directors).where(Director.last_name.ilike(search_pattern) | Director.first_name.ilike(search_pattern) | func.concat(Director.first_name, " ", Director.last_name).ilike(search_pattern))
    total_count = session.exec(statement).one()
    return total_count

def count_movies_by_min_rating(*, session: Session, min_rating: float) -> int:
    """Return the total number of movies whose average rating from active users meets the minimum."""
    movie_ids = select(Movie.id).join(Movie.reviews).join(User, Review.user_id == User.id).where(User.is_active == True).group_by(Movie.id).having(func.avg(Review.rating) >= min_rating).subquery()
    statement = select(func.count()).select_from(movie_ids)
    total_count = session.exec(statement).one()
    return total_count

def count_movies_ordered_by_rating(*, session: Session) -> int:
    """Return the total number of movies with at least one review from an active user."""
    statement = select(func.count(func.distinct(Movie.id))).select_from(Movie).join(Movie.reviews).join(User, Review.user_id == User.id).where(User.is_active == True)
    total_count = session.exec(statement).one()
    return total_count