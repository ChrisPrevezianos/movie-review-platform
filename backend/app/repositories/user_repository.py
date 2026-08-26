import uuid
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserUpdateMe
from pydantic import EmailStr
from app.core.security import get_password_hash
from sqlalchemy import func

def create_user(*, session: Session, user_create: UserCreate) -> User:
    """Create a user and store the password as a secure hash."""
    db_user = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_id(*, session: Session, user_id: uuid.UUID) -> User | None:
    session_user = session.get(User, user_id)
    return session_user

def get_user_by_email(*, session: Session, email: EmailStr) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user

def get_users(*, session: Session) -> list[User]:
    statement = select(User)
    session_users = session.exec(statement).all()
    return list(session_users)

def update_user(*, session: Session, db_user: User, user_update: UserUpdate) -> User:
    """Update user data, including password hashing when provided."""
    user_data = user_update.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user_me(*, session: Session, db_user: User, user_update: UserUpdateMe) -> User:
    """Update profile fields that a user is allowed to change."""
    user_data = user_update.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_hashed_password(*, session: Session, db_user: User, hashed_password: str) -> User:
    """Persist an already hashed password for the given user."""
    db_user.hashed_password = hashed_password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(*, session: Session, db_user: User) -> None:
    session.delete(db_user)
    session.commit()

def count_active_users(*, session: Session) -> int:
    """Return the number of active user accounts."""
    statement = select(func.count()).select_from(User).where(User.is_active == True)
    count = session.exec(statement).one()
    return count

def count_inactive_users(*, session: Session) -> int:
    """Return the number of inactive user accounts."""
    statement = select(func.count()).select_from(User).where(User.is_active == False)
    count = session.exec(statement).one()
    return count
