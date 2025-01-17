import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate, UserResponse
from src.utils.helpers import hash_password


def create_user(request: UserCreate, db: Session) -> UserResponse:
    """
    Create a new user in the database.
    """
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email is already registered.",
        )
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username is already taken.",
        )

    hashed_password = hash_password(request.password)
    new_user = User(
        user_id=str(uuid.uuid4()),
        username=request.username,
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        password_hash=hashed_password,
        address=request.address,
        phone_number=request.phone_number,
        role=request.role,
        social_links=request.social_links,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(
        user_id=str(new_user.user_id),
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role=new_user.role,
        address=new_user.address,
        phone_number=new_user.phone_number,
        social_links=new_user.social_links,
        password_hash=new_user.password_hash,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )


def update_user(user_id: str, request: UserUpdate, db: Session) -> UserResponse:
    """
    Update user information in the database.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    if request.first_name:
        user.first_name = request.first_name
    if request.last_name:
        user.last_name = request.last_name
    if request.address:
        user.address = request.address
    if request.phone_number:
        user.phone_number = request.phone_number
    if request.social_links:
        user.social_links = request.social_links

    db.commit()
    db.refresh(user)
    return UserResponse(
        user_id=str(user.user_id),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        address=user.address,
        phone_number=user.phone_number,
        social_links=user.social_links,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def get_user_by_id(user_id: str, db: Session) -> UserResponse:
    """
    Retrieve a user by ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return UserResponse(
        user_id=str(user.user_id),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        address=user.address,
        phone_number=user.phone_number,
        social_links=user.social_links,
        password_hash=user.password_hash,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
