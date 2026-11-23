import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRole


# Shared attributes across multiple schemas (Base class)
class UserBase(BaseModel):
    # EmailStr automatically validates if input is a valid email format (e.g., user@example.com)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150, description="User's full name")
    phone_number: str | None = Field(None, max_length=20, description="Contact phone number")


# Schema for Incoming Data: when a user registers or creates an account
class UserCreate(UserBase):
    # Plain text password sent by user; min_length=8 enforces strong password policy
    password: str = Field(..., min_length=8, description="Plain text password (min 8 chars)")
    # Defaults to CUSTOMER role unless specified
    role: UserRole = UserRole.CUSTOMER


# Schema for User Login request
class UserLogin(BaseModel):
    """Schema for incoming user authentication requests."""
    email: EmailStr
    password: str


# Schema for Updating User: all fields are optional because the user might only update their name
class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=2, max_length=150)
    phone_number: str | None = Field(None, max_length=20)
    password: str | None = Field(None, min_length=8)


# Schema for Outgoing Data: what the frontend receives in API responses
class UserResponse(UserBase):
    id: uuid.UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # IMPORTANT: from_attributes = True (formerly orm_mode in Pydantic v1)
    # This allows Pydantic to read data directly from a SQLAlchemy model object (e.g., user.id, user.email)
    model_config = ConfigDict(from_attributes=True)
