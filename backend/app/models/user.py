import enum
import uuid
from datetime import datetime, timezone

# Column types from SQLAlchemy to tell PostgreSQL what SQL data type to use
from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum
# PostgreSQL has a native high-performance UUID type
from sqlalchemy.dialects.postgresql import UUID
# Mapped is for Python type-hinting; mapped_column defines database column rules
from sqlalchemy.orm import Mapped, mapped_column

# Base is our parent declarative class that registers this model with SQLAlchemy
from app.core.database import Base


# We inherit from both 'str' and 'enum.Enum'.
# WHY 'str'? So FastAPI/Pydantic can convert it directly to JSON without needing .value
class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    OPERATOR = "operator"
    ADMIN = "admin"


# Inheriting from Base tells SQLAlchemy: "Create a database table from this class!"
class User(Base):
    # The actual SQL table name in PostgreSQL
    __tablename__ = "users"

    # UUID primary key: Prevents enumeration attacks (hackers guessing /users/1, /users/2)
    # default=uuid.uuid4: Automatically generates a random UUID whenever a new row is created
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # unique=True: DB rejects duplicate emails
    # index=True: Creates a B-Tree index in PostgreSQL so "SELECT * WHERE email = ?" is instant O(log N)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # We store the Bcrypt/Argon2 hash here, NEVER the plain text password
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # Optional phone number (str | None): used for bus booking SMS alerts
    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        default=None,
    )

    # Store role as an Enum in PostgreSQL with default 'customer'
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.CUSTOMER,
    )

    # Soft active flag: lets us deactivate/ban accounts without breaking past booking records
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Timestamp stored in UTC to avoid daylight saving and timezone confusion
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # onupdate: Automatically changes this timestamp whenever this row gets modified
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # __repr__ is what Python prints in the terminal when debugging: print(user)
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
