"""Database engine setup and initial application data seeding."""
from sqlmodel import Session, create_engine
from app.core.config import settings

# Import all models so SQLAlchemy can resolve relationships at runtime.
from app.models.actor import Actor
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.review import Review
from app.models.user import User

from app.schemas.user import UserCreate, UserUpdate
from app.schemas.genre import GenreCreate
from app.repositories import genre_repository as genre_repo
from app.repositories import user_repository as user_repo

engine = create_engine(str(settings.DATABASE_URL))

# Predefined movie genres inserted during database initialization.
INITIAL_GENRES = [
    "Action",
    "Adventure",
    "Animation",
    "Anime",
    "Biography",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Musical",
    "Mystery",
    "Psychological Thriller",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Superhero",
    "Thriller",
    "War",
    "Western",
]


def init_db(session: Session) -> None:
    """Initialize the database with the owner superuser and predefined genres."""
    user = user_repo.get_user_by_email(session=session, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            username="owner",
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = user_repo.create_user(session=session, user_create=user_in)
        user_update = UserUpdate(is_superuser=True)
        user_repo.update_user(session=session, db_user=user, user_update=user_update)

    for genre_name in INITIAL_GENRES:
        existing_genre = genre_repo.get_genre_by_name(session=session, genre_name=genre_name)
        if not existing_genre:
            genre = GenreCreate(name=genre_name)
            genre_repo.create_genre(session=session, genre_create=genre)