from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_current_user
from app.models.user import User
from app.schemas.token import Token, TokenRefreshRequest
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter()


# ---------------------------------------------------------------------------
# 1. User Registration Endpoint
# ---------------------------------------------------------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new customer, bus operator, or admin user. Hashes the password and persists to PostgreSQL.",
)
async def register(
    user_in: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    """
    HTTP POST /api/v1/auth/register
    1. Validates the incoming JSON body against UserCreate schema.
    2. Injects AuthService with an active database session.
    3. Hashes password with bcrypt and inserts into the database.
    4. Returns 201 Created with the UserResponse schema (password hash stripped).
    """
    user = await auth_service.register_user(user_in)
    return user


# ---------------------------------------------------------------------------
# 2. User Login Endpoint
# ---------------------------------------------------------------------------
@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticates credentials and returns JWT access and refresh tokens.",
)
async def login(
    login_data: UserLogin,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    """
    HTTP POST /api/v1/auth/login
    1. Looks up the user by email in PostgreSQL.
    2. Verifies the plain password against the stored bcrypt hash.
    3. Checks if the account is active.
    4. Issues a short-lived access token (with role claims) and a long-lived refresh token.
    """
    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    return auth_service.create_user_tokens(user)


# ---------------------------------------------------------------------------
# 3. Token Refresh Endpoint
# ---------------------------------------------------------------------------
@router.post(
    "/refresh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="Exchanges a valid refresh token for a newly issued access token.",
)
async def refresh_token(
    refresh_in: TokenRefreshRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    """
    HTTP POST /api/v1/auth/refresh
    1. Cryptographically verifies the refresh token's signature and expiry.
    2. Checks the user exists and is still active.
    3. Issues a new access token without requiring re-entering password.
    """
    return await auth_service.refresh_access_token(refresh_in.refresh_token)


# ---------------------------------------------------------------------------
# 4. Protected User Profile Endpoint
# ---------------------------------------------------------------------------
@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Current User Profile",
    description="Returns the profile of the authenticated user decoded from the Authorization Bearer token.",
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    HTTP GET /api/v1/auth/me
    - Protected route: requires 'Authorization: Bearer <token>' header.
    - get_current_user dependency decodes the token, extracts UUID, and loads User from DB.
    - If token is missing, expired, or invalid -> automatically returns 401 Unauthorized.
    """
    return current_user
