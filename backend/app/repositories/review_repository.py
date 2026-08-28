import uuid
import datetime
from sqlmodel import Session, select
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from sqlalchemy import func

def create_review(*, session: Session, review_create: ReviewCreate, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review:
    db_review = Review.model_validate(review_create, update={"user_id": user_id, "movie_id": movie_id})
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def get_review_by_id(*, session: Session, review_id: uuid.UUID) -> Review | None:
    session_review = session.get(Review, review_id)
    return session_review

def get_reviews(*, session: Session) -> list[Review]:
    statement = select(Review)
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

def get_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID) -> list[Review]:
    """Return all reviews for a movie, ordered by most recent activity.
    Uses updated_at when available, otherwise falls back to created_at.
    """
    statement = select(Review).where(Review.movie_id == movie_id).order_by(func.coalesce(Review.updated_at, Review.created_at).desc())
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def get_reviews_by_user_id(*, session: Session, user_id: uuid.UUID) -> list[Review]:
    """Return all reviews created by a user, ordered by most recent activity.
    Uses updated_at when available, otherwise falls back to created_at.
    """
    statement = select(Review).where(Review.user_id == user_id).order_by(func.coalesce(Review.updated_at, Review.created_at).desc())
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def get_review_by_user_and_movie_id(*, session: Session, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review | None:
    """Return a user's review for a specific movie, if one exists.
    Used to enforce the one-review-per-user-per-movie rule.
    """
    statement = select(Review).where(Review.user_id == user_id, Review.movie_id == movie_id)
    session_review = session.exec(statement).first()
    return session_review
