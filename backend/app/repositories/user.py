import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    """
    Data Access Layer for Users.
    Encapsulates all direct SQLAlchemy database queries for the 'users' table.
    """

    def __init__(self, session: AsyncSession):
        # We inject the database session through the constructor
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetch a single user by primary key UUID."""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        # scalar_one_or_none(): returns the User object if found, or None if not found
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a single user by unique email address."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate, hashed_password: str) -> User:
        """
        Creates and persists a new User record in PostgreSQL.
        """
        # Convert Pydantic schema to SQLAlchemy Model instance
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            phone_number=user_in.phone_number,
            role=user_in.role,
        )
        # Stage the new row in the session
        self.session.add(db_user)
        # Commit the transaction to save it permanently to PostgreSQL disk
        await self.session.commit()
        # Refresh to load PostgreSQL-generated values (id, created_at, updated_at)
        await self.session.refresh(db_user)
        return db_user
