import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token


class AuthService:
    """
    Business Logic Layer for User Authentication and Registration.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        # The service talks to the database exclusively through the repository
        self.user_repo = UserRepository(session)

    async def register_user(self, user_in: UserCreate) -> User:
        """
        Business Rule:
        1. Check if email already taken.
        2. Hash password with bcrypt.
        3. Save to database.
        """
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists in the system.",
            )

        hashed_pwd = hash_password(user_in.password)
        new_user = await self.user_repo.create(user_in=user_in, hashed_password=hashed_pwd)
        return new_user

    async def authenticate_user(self, email: str, password: str) -> User:
        """
        Business Rule:
        1. Look up user by email.
        2. Verify password against stored hash.
        3. Ensure user account is active.
        """
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This account has been deactivated. Please contact support.",
            )

        return user

    def create_user_tokens(self, user: User) -> Token:
        """Generates access and refresh tokens for a verified user."""
        access_token = create_access_token(subject=user.id, role=user.role.value)
        refresh_token = create_refresh_token(subject=user.id)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )

    async def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Validates refresh token and issues a new access token.
        """
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
            )

        try:
            user_id = uuid.UUID(str(user_id_str))
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token subject.",
            )

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive.",
            )

        new_access_token = create_access_token(subject=user.id, role=user.role.value)
        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )
