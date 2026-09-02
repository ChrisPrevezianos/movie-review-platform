"""Service functions for Movie business rules, filtering, ratings, and repository operations."""
import uuid
from sqlmodel import Session
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate
from app.repositories import movie_repository as movie_repo
from app.repositories import review_repository as review_repo
from fastapi import HTTPException, status

def create_movie(*, session: Session, movie_create: MovieCreate) -> Movie:
    """Create a movie unless the same title and release year already exist."""
    existing_title = movie_repo.get_movie_by_exact_title(session=session, title=movie_create.title)
    if existing_title:
        if any(movie.release_year == movie_create.release_year for movie in existing_title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The movie with this title and release year already exists in the system.",
            )
    return movie_repo.create_movie(session=session, movie_create=movie_create)

def get_movie_by_id(*, session: Session, movie_id: uuid.UUID) -> Movie | None:
    """Return a movie by ID, if it exists."""
    return movie_repo.get_movie_by_id(session=session, movie_id=movie_id)

def get_movies(*, session: Session, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies with pagination."""
    return movie_repo.get_movies(session=session, skip=skip, limit=limit)

def update_movie(*, session: Session, db_movie: Movie, movie_update: MovieUpdate) -> Movie:
    """Update a movie while preventing unchanged title/year values
    and duplicate title + release year combinations.
    """
    if movie_update.title is not None or movie_update.release_year is not None:
        if movie_update.title == db_movie.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new title must be different from the current title.",
            )
        movie_update.title = movie_update.title if movie_update.title is not None else db_movie.title
    
        if movie_update.release_year == db_movie.release_year:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new release year must be different from the current release year.",
            )
        movie_update.release_year = movie_update.release_year if movie_update.release_year is not None else db_movie.release_year
        
        existing_title = movie_repo.get_movie_by_exact_title(session=session, title=movie_update.title)
        if existing_title:
            if any(movie.release_year == movie_update.release_year for movie in existing_title):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The movie with this title and release year already exists in the system.",
                )
    return movie_repo.update_movie(session=session, db_movie=db_movie, movie_update=movie_update)

def delete_movie(*, session: Session, db_movie: Movie) -> None:
    """Delete a movie only if it has no associated reviews."""
    has_reviews = review_repo.has_reviews_by_movie_id(session=session, movie_id=db_movie.id)
    if has_reviews:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The movie cannot be deleted because it has reviews.",
        )
    movie_repo.delete_movie(session=session, db_movie=db_movie)

def get_movies_by_title(*, session: Session, title: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Search movies by partial title with pagination."""
    return movie_repo.get_movies_by_title(session=session, title=title, skip=skip, limit=limit)

def get_movies_by_release_year(*, session: Session, release_year: int, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies from a specific release year with pagination."""
    return movie_repo.get_movies_by_release_year(session=session, release_year=release_year, skip=skip, limit=limit)

def get_movies_by_age_rating(*, session: Session, age_rating: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies with the given age rating with pagination."""
    return movie_repo.get_movies_by_age_rating(session=session, age_rating=age_rating, skip=skip, limit=limit)

def get_movies_by_genre(*, session: Session, genre: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies in the given genre with pagination."""
    return movie_repo.get_movies_by_genre(session=session, genre=genre, skip=skip, limit=limit)

def get_movies_by_actor(*, session: Session, actor_name: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies matching an actor name with pagination."""
    return movie_repo.get_movies_by_actor(session=session, actor_name=actor_name, skip=skip, limit=limit)

def get_movies_by_director(*, session: Session, director_name: str, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies matching a director name with pagination."""
    return movie_repo.get_movies_by_director(session=session, director_name=director_name, skip=skip, limit=limit)

def get_movies_by_min_rating(*, session: Session, min_rating: float, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return movies whose average rating from active users meets the minimum, with pagination."""
    return movie_repo.get_movies_by_min_rating(session=session, min_rating=min_rating, skip=skip, limit=limit)

def get_movies_ordered_by_rating(*, session: Session, skip: int = 0, limit: int = 10) -> list[Movie]:
    """Return reviewed movies ordered by average rating from active users, with pagination."""
    return movie_repo.get_movies_ordered_by_rating(session=session, skip=skip, limit=limit)

def get_top_rated_movies(*, session: Session, limit: int = 10) -> list[Movie]:
    """Return the highest-rated movies using reviews from active users, up to the given limit."""
    return movie_repo.get_top_rated_movies(session=session, limit=limit)

def count_movies(*, session: Session) -> int:
    """Return the total number of movies."""
    return movie_repo.count_movies(session=session)

def count_movies_by_title(*, session: Session, title: str) -> int:
    """Return the total number of movies matching the partial title search."""
    return movie_repo.count_movies_by_title(session=session, title=title)

def count_movies_by_release_year(*, session: Session, release_year: int) -> int:
    """Return the total number of movies from the given release year."""
    return movie_repo.count_movies_by_release_year(session=session, release_year=release_year)

def count_movies_by_age_rating(*, session: Session, age_rating: str) -> int:
    """Return the total number of movies with the given age rating."""
    return movie_repo.count_movies_by_age_rating(session=session, age_rating=age_rating)

def count_movies_by_genre(*, session: Session, genre: str) -> int:
    """Return the total number of movies in the given genre."""
    return movie_repo.count_movies_by_genre(session=session, genre=genre)

def count_movies_by_actor(*, session: Session, actor_name: str) -> int:
    """Return the total number of distinct movies matching the actor name search."""
    return movie_repo.count_movies_by_actor(session=session, actor_name=actor_name)

def count_movies_by_director(*, session: Session, director_name: str) -> int:
    """Return the total number of distinct movies matching the director name search."""
    return movie_repo.count_movies_by_director(session=session, director_name=director_name)

def count_movies_by_min_rating(*, session: Session, min_rating: float) -> int:
    """Return the total number of movies whose average rating from active users meets the minimum."""
    return movie_repo.count_movies_by_min_rating(session=session, min_rating=min_rating)

def count_movies_ordered_by_rating(*, session: Session) -> int:
    """Return the total number of movies with at least one review from an active user."""
    return movie_repo.count_movies_ordered_by_rating(session=session)