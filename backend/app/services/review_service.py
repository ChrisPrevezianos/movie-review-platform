"""Service functions for Review business rules and repository operations."""
import uuid
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.repositories import review_repository as review_repo
from app.repositories import movie_repository as movie_repo

def create_review(*, session: Session, review_create: ReviewCreate, user_id: uuid.UUID, movie_id: uuid.UUID) -> Review:
    """Create a review if the movie exists and the user has not already reviewed it."""
    existing_movie_id = movie_repo.get_movie_by_id(session=session, movie_id=movie_id)
    if existing_movie_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The movie does not exist.",
        )

    existing_review = review_repo.get_review_by_user_and_movie_id(session=session, user_id=user_id, movie_id=movie_id)
    if existing_review is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user has already reviewed this movie.",
        )
    return review_repo.create_review(session=session, review_create=review_create, user_id=user_id, movie_id=movie_id)

def get_review_by_id(*, session: Session, review_id: uuid.UUID) -> Review | None:
    """Return a review by ID only if its author is active."""
    return review_repo.get_review_by_id(session=session, review_id=review_id)

def get_reviews(*, session: Session, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews from active users with pagination."""
    return review_repo.get_reviews(session=session, skip=skip, limit=limit)

def update_review(*, session: Session, db_review: Review, review_update: ReviewUpdate, user_id: uuid.UUID) -> Review:
    """Update a review only if it belongs to the current user.
    Rejects empty update requests.
    """
    if db_review.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this review.",
        )
    if not review_update.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No review data provided for update.",
        )
    return review_repo.update_review(session=session, db_review=db_review, review_update=review_update)

def delete_review(*, session: Session, db_review: Review, user_id: uuid.UUID) -> None:
    """Delete a review only if it belongs to the current user."""
    if db_review.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this review.",
        )
    review_repo.delete_review(session=session, db_review=db_review)

def get_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews from active users for a movie with pagination."""
    return review_repo.get_reviews_by_movie_id(session=session, movie_id=movie_id, skip=skip, limit=limit)

def get_reviews_by_user_id(*, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews created by an active user with pagination."""
    return review_repo.get_reviews_by_user_id(session=session, user_id=user_id, skip=skip, limit=limit)

def get_admin_reviews(*, session: Session, user_id: uuid.UUID | None = None, movie_id: uuid.UUID | None = None, skip: int = 0, limit: int = 10) -> list[Review]:
    """Return reviews for admin, including reviews from inactive users.
    Optionally filters by user and/or movie and applies pagination.
    """
    return review_repo.get_admin_reviews(session=session, user_id=user_id, movie_id=movie_id, skip=skip, limit=limit)

def count_reviews(*, session: Session) -> int:
    """Return the total number of reviews created by active users."""
    return review_repo.count_reviews(session=session)

def count_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID) -> int:
    """Return the total number of reviews from active users for a movie."""
    return review_repo.count_reviews_by_movie_id(session=session, movie_id=movie_id)

def count_reviews_by_user_id(*, session: Session, user_id: uuid.UUID) -> int:
    """Return the total number of reviews created by an active user."""
    return review_repo.count_reviews_by_user_id(session=session, user_id=user_id)

def count_admin_reviews(*, session: Session, user_id: uuid.UUID | None = None, movie_id: uuid.UUID | None = None) -> int:
    """Return the total number of reviews for admin, including inactive-user reviews.
    Optionally filters by user and/or movie.
    """
    return review_repo.count_admin_reviews(session=session, user_id=user_id, movie_id=movie_id)