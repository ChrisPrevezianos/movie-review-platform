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
    return movie_repo.get_movie_by_id(session=session, movie_id=movie_id)

def get_movies(*, session: Session) -> list[Movie]:
    return movie_repo.get_movies(session=session)

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

def delete_movie(*, session: Session, db_Movie: Movie) -> None:
    """Delete a movie only if it has no associated reviews."""
    reviews = review_repo.get_reviews_by_movie_id(session=session, movie_id=db_Movie.id)
    if reviews:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The movie cannot be deleted because it has reviews.",
        )
    movie_repo.delete_movie(session=session, db_movie=db_Movie)

def get_movies_by_title(*, session: Session, title: str) -> list[Movie]:
    return movie_repo.get_movies_by_title(session=session, title=title)

def get_movies_by_release_year(*, session: Session, release_year: int) -> list[Movie]:
    return movie_repo.get_movies_by_release_year(session=session, release_year=release_year)

def get_movies_by_age_rating(*, session: Session, age_rating: str) -> list[Movie]:
    return movie_repo.get_movies_by_age_rating(session=session, age_rating=age_rating)

def get_movies_by_genre(*, session: Session, genre: str) -> list[Movie]:
    return movie_repo.get_movies_by_genre(session=session, genre=genre)

def get_movies_by_actor(*, session: Session, actor_name: str) -> list[Movie]:
    return movie_repo.get_movies_by_actor(session=session, actor_name=actor_name)

def get_movies_by_director(*, session: Session, director_name: str) -> list[Movie]:
    return movie_repo.get_movies_by_director(session=session, director_name=director_name)

def get_movies_by_min_rating(*, session: Session, min_rating: float) -> list[Movie]:
    return movie_repo.get_movies_by_min_rating(session=session, min_rating=min_rating)

def get_movies_ordered_by_rating(*, session: Session) -> list[Movie]:
    return movie_repo.get_movies_ordered_by_rating(session=session)

def get_top_rated_movies(*, session: Session, limit: int = 10) -> list[Movie]:
    return movie_repo.get_top_rated_movies(session=session, limit=limit)