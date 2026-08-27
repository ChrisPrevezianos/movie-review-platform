import uuid
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UpdatePassword, UserUpdate, UserUpdateMe
from app.repositories import user_repository as user_repo
from app.core.security import verify_password, get_password_hash, DUMMY_HASH
from pydantic import EmailStr

def create_user(*, session: Session, user_create: UserCreate) -> User:
    """Create a user after validating unique email and username."""
    existing_email = user_repo.get_user_by_email(session=session, email=user_create.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    existing_username = user_repo.get_user_by_username(session=session, username=user_create.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    return user_repo.create_user(session=session, user_create=user_create)

def get_user_by_id(*, session: Session, user_id: uuid.UUID) -> User | None:
    return user_repo.get_user_by_id(session=session, user_id=user_id)

def get_users(*, session: Session) -> list[User]:
    return user_repo.get_users(session=session)

def update_user(*, session: Session, db_user: User, user_update: UserUpdate) -> User:
    """Update user data after validating email and username changes."""
    if user_update.email:
        if user_update.email == db_user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new email must be different from the current email.",
            )

        existing_email = user_repo.get_user_by_email(session=session, email=user_update.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )

    if user_update.username:
        if user_update.username == db_user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new username must be different from the current username.",
            )

        existing_username = user_repo.get_user_by_username(session=session, username=user_update.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this username already exists in the system.",
            )

    return user_repo.update_user(session=session, db_user=db_user, user_update=user_update)

def update_user_me(*, session: Session, db_user: User, user_update: UserUpdateMe) -> User:
    """Update profile fields that the current user is allowed to change."""
    if user_update.email:
        if user_update.email == db_user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new email must be different from the current email.",
            )

        existing_email = user_repo.get_user_by_email(session=session, email=user_update.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )

    if user_update.username:
        if user_update.username == db_user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The new username must be different from the current username.",
            )

        existing_username = user_repo.get_user_by_username(session=session, username=user_update.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this username already exists in the system.",
            )

    return user_repo.update_user_me(session=session, db_user=db_user, user_update=user_update)

def change_password(*, session: Session, db_user: User, user_update: UpdatePassword) -> User:
    """Change a user's password after verifying the current password."""
    current_password = user_update.current_password
    is_valid, _ = verify_password(current_password, db_user.hashed_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The current password is incorrect.",
        )

    if user_update.new_password == user_update.current_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The new password must be different from the current password.",
        )
    
    hashed_password = get_password_hash(user_update.new_password)
    return user_repo.update_hashed_password(session=session, db_user=db_user, hashed_password=hashed_password)


def deactivate_user(*, session: Session, db_user: User) -> User:
    """Deactivate a user account while preserving its historical data."""
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "This account is already deactivated.",
        )
    return user_repo.deactivate_user(session=session, db_user=db_user)

def reactivate_user(*, session: Session, db_user: User) -> User:
    """Reactivate a previously deactivated user account."""
    if db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "This account is already active.",
        )
    return user_repo.reactivate_user(session=session, db_user=db_user)

def count_active_users(*, session: Session) -> int:
    return user_repo.count_active_users(session=session)

def count_inactive_users(*, session: Session) -> int:
    return user_repo.count_inactive_users(session=session)

def authenticate_user(*, session: Session, email: EmailStr, password: str) -> User | None:
    """Authenticate an active user by email and password."""
    db_user = user_repo.get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "This account is no longer available.",
        )
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user
