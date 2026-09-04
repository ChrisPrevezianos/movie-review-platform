"""API routes for user registration, profiles, account management, and administration."""
import uuid
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.schemas.user import UserPublic, UserCreate, UserUpdate, UserUpdateMe, UsersPublic, UserOwnData, UpdatePassword, UserPrivateData, UsersPrivateData
from app.services import user_service


router = APIRouter(prefix="/users", tags=["users"])

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

@router.get("", response_model=UsersPublic)
def get_users(*, session: SessionDep, page: int = 1, page_size: int = 10) -> UsersPublic:
    """Return public user profiles with pagination."""
    skip = paginated_check(page=page, page_size=page_size)
    users = user_service.get_active_users(session=session, skip=skip, limit=page_size)
    total_count = user_service.count_active_users(session=session)
    users_public = [UserPublic.model_validate(user) for user in users]
    return UsersPublic(users=users_public, count=total_count)

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(*, session: SessionDep, user_in: UserCreate) -> UserPublic:
    """Register a new user account."""
    return user_service.create_user(session=session, user_create=user_in)

@router.get("/me", response_model=UserOwnData)
def read_user_me(current_user: CurrentUser) -> UserOwnData:
    """Return profile data for the currently authenticated user."""
    return current_user

@router.patch("/me", response_model=UserOwnData, status_code=status.HTTP_200_OK)
def update_user_me(*, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser) -> UserOwnData:
    """Update the currently authenticated user's profile."""
    return user_service.update_user_me(session=session, db_user=current_user, user_update=user_in)

@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def update_password_me(*, session: SessionDep, body: UpdatePassword, current_user: CurrentUser) -> None:
    """Change the currently authenticated user's password."""
    user_service.change_password(session=session, db_user=current_user, user_update=body)

@router.patch("/me/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_user_me(*, session: SessionDep, current_user: CurrentUser) -> None:
    """Deactivate the currently authenticated user's account."""
    if current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super users are not allowed to deactivate themselves"
        )
    user_service.deactivate_user(session=session, db_user=current_user)

@router.get("/admin", response_model=UsersPrivateData, dependencies=[Depends(get_current_active_superuser)])
def get_users_private_dada(*, session: SessionDep, page: int = 1, page_size: int = 10) -> UsersPrivateData:
    """Return private user account data with pagination. Admin only."""
    skip = paginated_check(page=page, page_size=page_size)
    users = user_service.get_users(session=session, skip=skip, limit=page_size)
    total_count = user_service.count_users(session=session)
    users_public = [UserPrivateData.model_validate(user) for user in users]
    return UsersPrivateData(users=users_public, count=total_count)

@router.get("/email", response_model=UserPrivateData, dependencies=[Depends(get_current_active_superuser)])
def get_user_by_email(*, session: SessionDep, email: EmailStr) -> UserPrivateData:
    """Return a user account by exact email match. Admin only."""
    existing_user = user_service.get_user_by_email(session=session, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system",
        )
    return existing_user

@router.get("/username", response_model=UserPrivateData, dependencies=[Depends(get_current_active_superuser)])
def get_user_by_username(*, session: SessionDep, username: str) -> UserPrivateData:
    """Return a user account by exact username match. Admin only."""
    existing_user = user_service.get_user_by_username(session=session, username=username)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    return existing_user

@router.get("/active-users", response_model=UsersPrivateData, dependencies=[Depends(get_current_active_superuser)])
def get_active_users(*, session: SessionDep, page: int = 1, page_size: int = 10) -> UsersPrivateData:
    """Return active user accounts with pagination. Admin only."""
    skip = paginated_check(page=page, page_size=page_size)
    users = user_service.get_active_users(session=session, skip=skip, limit=page_size)
    total_count = user_service.count_active_users(session=session)
    users_public = [UserPrivateData.model_validate(user) for user in users]
    return UsersPrivateData(users=users_public, count=total_count)

@router.get("/inactive-users", response_model=UsersPrivateData, dependencies=[Depends(get_current_active_superuser)])
def get_inactive_users(*, session: SessionDep, page: int = 1, page_size: int = 10) -> UsersPrivateData:
    """Return inactive user accounts with pagination. Admin only."""
    skip = paginated_check(page=page, page_size=page_size)
    users = user_service.get_inactive_users(session=session, skip=skip, limit=page_size)
    total_count = user_service.count_inactive_users(session=session)
    users_public = [UserPrivateData.model_validate(user) for user in users]
    return UsersPrivateData(users=users_public, count=total_count)

@router.get("/{user_id}", response_model=UserPrivateData, dependencies=[Depends(get_current_active_superuser)])
def get_user_by_id(*, session: SessionDep, user_id: uuid.UUID) -> UserPrivateData:
    """Return a user account by ID. Admin only."""
    existing_user = user_service.get_user_by_id(session=session, user_id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    return existing_user

@router.patch("/{user_id}", response_model=UserPrivateData, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_superuser)])
def update_user(*, session: SessionDep, user_id: uuid.UUID, user_in: UserUpdate, current_user: CurrentUser) -> UserPrivateData:
    """Update a user account. Admin only."""
    existing_user = user_service.get_user_by_id(session=session, user_id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    if existing_user == current_user and user_in.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user cannot deactivate themselves"
        )
    return user_service.update_user(session=session, db_user=existing_user, user_update=user_in)

@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_superuser)])
def deactivate_user(*, session: SessionDep, user_id: uuid.UUID, current_user: CurrentUser) -> None:
    """Deactivate a user account without deleting its data. Admin only."""
    existing_user = user_service.get_user_by_id(session=session, user_id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    if existing_user == current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super users are not allowed to deactivate themselves"
        )
    user_service.deactivate_user(session=session, db_user=existing_user)
    
@router.patch("/{user_id}/reactivate", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_superuser)])
def reactivate_user(*, session: SessionDep, user_id: uuid.UUID) -> None:
    """Reactivate a previously deactivated user account. Admin only."""
    existing_user = user_service.get_user_by_id(session=session, user_id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    user_service.reactivate_user(session=session, db_user=existing_user)