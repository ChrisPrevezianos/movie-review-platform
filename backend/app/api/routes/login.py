"""API routes for user authentication and access-token validation."""
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import CurrentUser, SessionDep
from app.core import security
from app.core.config import settings
from app.schemas.auth import Token
from app.schemas.user import UserOwnData
from app.services import user_service

router = APIRouter(tags=["login"])

@router.post("/login/access-token")
def login_access_token(*,session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Authenticate a user and return a JWT access token."""
    user = user_service.authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=security.create_access_token(user.id, expires_delta=access_token_expires))

@router.post("/login/test-token", response_model=UserOwnData)
def test_token(current_user: CurrentUser) -> UserOwnData:
    """Validate the current access token and return the authenticated user's profile."""
    return current_user
