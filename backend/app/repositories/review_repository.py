import uuid
from sqlmodel import Session, select
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

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
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def delete_review(*, session: Session, db_review: Review) -> None:
    session.delete(db_review)
    session.commit()

def get_reviews_by_movie_id(*, session: Session, movie_id: uuid.UUID) -> list[Review]:
    statement = select(Review).where(Review.movie_id == movie_id)
    session_reviews = session.exec(statement).all()
    return list(session_reviews)

def get_reviews_by_user_id(*, session: Session, user_id: uuid.UUID) -> list[Review]:
    statement = select(Review).where(Review.user_id == user_id)
    session_reviews = session.exec(statement).all()
    return list(session_reviews)