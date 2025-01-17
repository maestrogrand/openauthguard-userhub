import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "user_service"}

    user_id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    role = Column(
        Enum("user", "admin", name="user_roles"),
        default="user",
        nullable=False,
    )
    social_links = Column(JSONB, nullable=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
