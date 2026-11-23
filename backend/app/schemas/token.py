from pydantic import BaseModel
from app.schemas.user import UserResponse


class Token(BaseModel):
    """Schema returned on successful login or token refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse | None = None


class TokenPayload(BaseModel):
    """Schema representing data stored inside the decoded JWT."""
    sub: str | None = None
    role: str | None = None
    type: str | None = None


class TokenRefreshRequest(BaseModel):
    """Schema for requesting a new access token using a refresh token."""
    refresh_token: str
