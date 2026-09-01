"""API routes for Review management, retrieval, pagination, and administration."""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.schemas import ReviewPublic, ReviewsPublic, ReviewCreate, ReviewUpdate
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["reviews"])

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


@router.get("", response_model=ReviewsPublic)
def get_reviews(*, session: SessionDep, page: int = 1, page_size: int = 10) -> ReviewsPublic:
    """Return reviews from active users with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    reviews = review_service.get_reviews(session=session, skip=skip, limit=page_size)
    total_count = review_service.count_reviews(session=session)
    reviews_public = [ReviewPublic.model_validate(review) for review in reviews]
    return ReviewsPublic(reviews=reviews_public, count=total_count)

@router.get("/admin", response_model=ReviewsPublic, dependencies=[Depends(get_current_active_superuser)])
def get_admin_reviews(*, session: SessionDep, user_id: uuid.UUID | None = None, movie_id: uuid.UUID | None = None, page: int = 1, page_size: int = 10) -> ReviewsPublic:
    """Return reviews for admin, including inactive-user reviews.
    Optionally filters by user and/or movie and applies pagination.
    Requires superuser privileges.
    """
    skip = paginated_check(page=page, page_size=page_size)
    reviews = review_service.get_admin_reviews(session=session, user_id=user_id, movie_id=movie_id, skip=skip, limit=page_size)
    total_count = review_service.count_admin_reviews(session=session, user_id=user_id, movie_id=movie_id)
    reviews_public = [ReviewPublic.model_validate(review) for review in reviews]
    return ReviewsPublic(reviews=reviews_public, count= total_count)

@router.get("/{review_id}", response_model=ReviewPublic)
def get_review(*, session: SessionDep, review_id: uuid.UUID) -> ReviewPublic:
    """Return a review by ID only if its author is active, or raise 404."""
    review = review_service.get_review_by_id(session=session, review_id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review

@router.get("/movie/{movie_id}", response_model=ReviewsPublic)
def get_reviews_by_movie(*, session: SessionDep, movie_id: uuid.UUID, page: int = 1, page_size: int = 10) -> ReviewsPublic:
    """Return reviews from active users for a movie with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    reviews = review_service.get_reviews_by_movie_id(session=session, movie_id=movie_id, skip=skip, limit=page_size)
    total_count = review_service.count_reviews_by_movie_id(session=session, movie_id=movie_id)
    reviews_public = [ReviewPublic.model_validate(review) for review in reviews]
    return ReviewsPublic(reviews=reviews_public, count=total_count)

@router.get("/user/{user_id}", response_model=ReviewsPublic)
def get_reviews_by_user(*, session: SessionDep, user_id: uuid.UUID, page: int = 1, page_size: int = 10) -> ReviewsPublic:
    """Return reviews created by an active user with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    reviews = review_service.get_reviews_by_user_id(session=session, user_id=user_id, skip=skip, limit=page_size)
    total_count = review_service.count_reviews_by_user_id(session=session, user_id=user_id)
    reviews_public = [ReviewPublic.model_validate(review) for review in reviews]
    return ReviewsPublic(reviews=reviews_public, count=total_count)

@router.post("/movie/{movie_id}", response_model=ReviewPublic, status_code=status.HTTP_201_CREATED)
def create_review(*, session: SessionDep, current_user: CurrentUser, review_in: ReviewCreate, movie_id: uuid.UUID) -> ReviewPublic:
    """Create a review for the current authenticated user."""
    return review_service.create_review(session=session, review_create=review_in, user_id=current_user.id, movie_id=movie_id)

@router.patch("/{review_id}", response_model=ReviewPublic, status_code=status.HTTP_200_OK)
def update_review(*, session: SessionDep, current_user: CurrentUser, review_id: uuid.UUID, review_in: ReviewUpdate) -> ReviewPublic:
    """Update a review only if it belongs to the current authenticated user."""
    review = review_service.get_review_by_id(session=session, review_id=review_id)
    if  not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review_service.update_review(session=session, db_review=review, review_update=review_in, user_id=current_user.id)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(*, session: SessionDep, current_user: CurrentUser, review_id: uuid.UUID) -> None:
    """Delete a review only if it belongs to the current authenticated user."""
    review = review_service.get_review_by_id(session=session, review_id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    review_service.delete_review(session=session, db_review=review, user_id=current_user.id)