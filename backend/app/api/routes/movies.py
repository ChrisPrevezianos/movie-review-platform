"""API routes for Movie retrieval, filtering, ratings, pagination, and administration."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import SessionDep, get_current_active_superuser
from app.schemas.movie import MoviesPublic, MoviePublic, MovieCreate, MovieUpdate, AgeRating
from app.services import movie_service

router = APIRouter(prefix="/movies", tags=["movies"])

def paginated_check(*, page: int, page_size: int) -> int:
    """Validate pagination parameters and return the calculated offset."""
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
    return (page - 1) * page_size

@router.get("", response_model=MoviesPublic)
def get_movies(*, session: SessionDep, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    movies = movie_service.get_movies(session=session, skip=skip, limit=page_size)
    total_count = movie_service.count_movies(session=session)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/title", response_model=MoviesPublic)
def get_movies_by_title(*, session: SessionDep, title: str, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Search movies by partial title with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    title = title.strip()
    if title == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty"
        )
    movies = movie_service.get_movies_by_title(session=session, title=title, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_title(session=session, title=title)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/release-year", response_model=MoviesPublic)
def get_movies_by_release_year(*, session: SessionDep, release_year: int, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies from a specific release year with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    movies = movie_service.get_movies_by_release_year(session=session, release_year=release_year, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_release_year(session=session, release_year=release_year)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/age-rating", response_model=MoviesPublic)
def get_movies_by_age_rating(*, session: SessionDep, age_rating: AgeRating, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies with the given age rating with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    movies = movie_service.get_movies_by_age_rating(session=session, age_rating=age_rating, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_age_rating(session=session, age_rating=age_rating)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/genre", response_model=MoviesPublic)
def get_movies_by_genre(*, session: SessionDep, genre: str, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies in the given genre with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    movies = movie_service.get_movies_by_genre(session=session, genre=genre, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_genre(session=session, genre=genre)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/actor", response_model=MoviesPublic)
def get_movies_by_actor(*, session: SessionDep, actor: str, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies matching an actor name with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    actor = actor.strip()
    if actor == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Actor cannot be empty"
        )
    movies = movie_service.get_movies_by_actor(session=session, actor_name=actor, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_actor(session=session, actor_name=actor)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/director", response_model=MoviesPublic)
def get_movies_by_director(*, session: SessionDep, director: str, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies matching a director name with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    director = director.strip()
    if director == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Director cannot be empty"
        )
    movies = movie_service.get_movies_by_director(session=session, director_name=director, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_director(session=session, director_name=director)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/min-rating", response_model=MoviesPublic)
def get_movies_by_min_rating(*, session: SessionDep, min_rating: 
    float, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return movies meeting the minimum average rating, with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    if min_rating < 1 or min_rating > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Min rating must be between 1 and 10"
        )
    movies = movie_service.get_movies_by_min_rating(session=session, min_rating=min_rating, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_by_min_rating(session=session, min_rating=min_rating)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/rating", response_model=MoviesPublic)
def get_movies_ordered_by_rating(*, session: SessionDep, page: int = 1, page_size: int = 10) -> MoviesPublic:
    """Return reviewed movies ordered by average rating, with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    movies = movie_service.get_movies_ordered_by_rating(session=session, skip=skip, limit=page_size)
    total_count = movie_service.count_movies_ordered_by_rating(session=session)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=total_count)

@router.get("/top-rated", response_model=MoviesPublic)
def get_top_rated_movies(*, session: SessionDep, limit: int = 10) -> MoviesPublic:
    """Return the highest-rated movies up to the requested limit."""
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be greater than or equal to 1"
        )
    if limit > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit cannot be greater than 50"
        )
    movies = movie_service.get_top_rated_movies(session=session, limit=limit)
    movies_public = [MoviePublic.model_validate(movie) for movie in movies]
    return MoviesPublic(movies=movies_public, count=len(movies))

@router.get("/{movie_id}", response_model=MoviePublic)
def get_movie(*, session: SessionDep, movie_id: uuid.UUID) -> MoviePublic:
    """Return a movie by ID or raise 404 if it does not exist."""
    movie = movie_service.get_movie_by_id(session=session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie

@router.post("", response_model=MoviePublic, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_superuser)])
def create_movie(*, session: SessionDep, movie_in: MovieCreate) -> MoviePublic:
    """Create a movie with selected genres. Admin only."""
    if len(movie_in.genre_ids) != len(set(movie_in.genre_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more genre IDs are duplicated."
        )
    return movie_service.create_movie(session=session, movie_create=movie_in)

@router.patch("/{movie_id}", response_model=MoviePublic, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_superuser)])
def update_movie(*, session: SessionDep, movie_id: uuid.UUID, movie_in: MovieUpdate) -> MoviePublic:
    """Update an existing movie and optionally its genres. Admin only."""
    movie = movie_service.get_movie_by_id(session=session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    if movie_in.genre_ids is not None and len(movie_in.genre_ids) != len(set(movie_in.genre_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more genre IDs are duplicated."
        )
    return movie_service.update_movie(session=session, db_movie=movie, movie_update=movie_in)

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_superuser)])
def delete_movie(*, session: SessionDep, movie_id: uuid.UUID) -> None:
    """Delete an existing movie. Admin only."""
    movie = movie_service.get_movie_by_id(session=session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    movie_service.delete_movie(session=session, db_movie=movie)