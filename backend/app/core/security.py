from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
import jwt

from app.core.config import settings


# ---------------------------------------------------------------------------
# Password Hashing Functions
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt with automatic salting.
    bcrypt operates on bytes, so we encode/decode to utf-8 strings.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches the stored bcrypt hash.
    Returns True if valid, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ---------------------------------------------------------------------------
# JWT Token Functions
# ---------------------------------------------------------------------------

def create_access_token(subject: Any, role: str, expires_delta: timedelta | None = None) -> str:
    """
    Generates a signed JWT Access Token containing user ID ('sub') and role.
    Short-lived token used for authenticating API requests.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Payload (Claims): data embedded inside the token
    to_encode = {
        "exp": expire,          # Expiration timestamp
        "sub": str(subject),    # Subject (usually User UUID)
        "role": str(role),      # User role for RBAC checks
        "type": "access",
    }

    # Cryptographically sign the payload with our SECRET_KEY
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: Any) -> str:
    """
    Generates a longer-lived Refresh Token used to obtain a new access token
    when the current access token expires.
    """
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Decodes and verifies the signature of a JWT token.
    Returns the payload dictionary if valid, or None if expired/tampered with.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
