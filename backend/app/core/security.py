"""Security utilities for password hashing, password verification, and JWT access tokens."""
import jwt
from datetime import UTC, datetime, timedelta
from typing import Any
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.config import settings

password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)

ALGORITHM = "HS256"

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    """Create and encode a JWT access token for the given subject."""
    expire = datetime.now(UTC) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> tuple[bool, str | None]:
    """Verify a plain password and return an updated hash when needed."""
    return password_hash.verify_and_update(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password for secure storage."""
    return password_hash.hash(password)