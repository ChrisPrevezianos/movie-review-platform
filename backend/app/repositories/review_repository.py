"""Repository functions for Review database operations, public queries, admin queries, and pagination."""
import uuid
import datetime
from sqlmodel import Session, select
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate
from sqlalchemy import func

def create_review(*, session: Session, review_create: ReviewCreate, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review:
    db_review = Review.model_validate(review_create, update={"user_id": user_id, "movie_id": movie_id})
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def get_review_by_id(*, session: Session, review_id: uuid.UUID) -> Review | None:
    """Return a review by ID only if its author is active."""
    statement = select(Review).join(User).where(User.is_active == True, Review.id == review_id)
    session_review = session.exec(statement).first()
    return session_review

def get_reviews(*, session: Session, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews from active users with pagination, ordered by most recent activity."""
    statement = select(Review).join(User).where(User.is_active == True).order_by(func.coalesce(Review.updated_at, Review.created_at).desc(), Review.id.desc()).offset(skip).limit(limit)
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def update_review(*, session: Session, db_review: Review, review_update: ReviewUpdate) -> Review:
    review_data = review_update.model_dump(exclude_unset=True)
    db_review.sqlmodel_update(review_data)
    db_review.updated_at = datetime.datetime.now(datetime.timezone.utc)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def delete_review(*, session: Session, db_review: Review) -> None:
    session.delete(db_review)
    session.commit()

def get_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews from active users for a movie with pagination, ordered by most recent activity.
    Uses updated_at when available, otherwise falls back to created_at.
    """
    statement = select(Review).join(User).where(User.is_active == True, Review.movie_id == movie_id).order_by(func.coalesce(Review.updated_at, Review.created_at).desc(), Review.id.desc()).offset(skip).limit(limit)
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def get_reviews_by_user_id(*, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews from an active user with pagination, ordered by most recent activity.
    Uses updated_at when available, otherwise falls back to created_at.
    """
    statement = select(Review).join(User).where(User.is_active == True, Review.user_id == user_id).order_by(func.coalesce(Review.updated_at, Review.created_at).desc(), Review.id.desc()).offset(skip).limit(limit)
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def get_review_by_user_and_movie_id(*, session: Session, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review | None:
    """Return a user's review for a specific movie, regardless of account status.
    Used to enforce the one-review-per-user-per-movie rule.
    """
    statement = select(Review).where(Review.user_id == user_id, Review.movie_id == movie_id)
    session_review = session.exec(statement).first()
    return session_review

def get_admin_reviews(*, session: Session, user_id: uuid.UUID | None = None, movie_id: uuid.UUID | None = None, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews for admin, including reviews from inactive users.
    Optionally filters by user and/or movie and applies pagination.
    """
    statement = select(Review)
    if user_id is not None:
        statement = statement.where(Review.user_id == user_id)
    if movie_id is not None:
        statement = statement.where(Review.movie_id == movie_id)
    
    statement = (statement.order_by(func.coalesce(Review.updated_at, Review.created_at).desc(), Review.id.desc()).offset(skip).limit(limit))
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def has_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID) -> bool:
    """Return whether any review exists for a movie, regardless of user account status.
    Used to preserve review history when deciding whether a movie can be deleted.
    """
    statement  = select(Review).where(Review.movie_id == movie_id)
    session_reviews = session.exec(statement).first()
    return bool(session_reviews)

def count_reviews(*, session: Session) -> int:
    """Return the total number of reviews created by active users."""
    statement = select(func.count()).select_from(Review).join(User).where(User.is_active == True)
    total_count = session.exec(statement).one()
    return total_count

def count_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID) -> int:
    """Return the total number of reviews from active users for a movie."""
    statement = select(func.count()).select_from(Review).join(User).where(User.is_active == True, Review.movie_id == movie_id)
    total_count = session.exec(statement).one()
    return total_count

def count_reviews_by_user_id(*, session: Session, user_id: uuid.UUID) -> int:
    """Return the total number of reviews created by an active user."""
    statement = select(func.count()).select_from(Review).join(User).where(User.is_active == True, Review.user_id == user_id)
    total_count = session.exec(statement).one()
    return total_count

def count_admin_reviews(*, session: Session, user_id: uuid.UUID | None = None, movie_id: uuid.UUID | None = None) -> int:
    """Return the total number of reviews for admin, including inactive-user reviews.
    Optionally filters by user and/or movie.
    """
    statement = select(func.count()).select_from(Review)
    if user_id is not None:
        statement = statement.where(Review.user_id == user_id)
    if movie_id is not None:
        statement = statement.where(Review.movie_id == movie_id)

    total_count = session.exec(statement).one()
    return total_count