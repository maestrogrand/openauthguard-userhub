from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.users.models import User
from src.users.schemas import UserCreate, UserResponse, UserUpdate
from src.users.services import create_user, get_user_by_id, update_user

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/register", response_model=UserResponse)
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new individual user.
    """
    return create_user(request, db)


user_router = APIRouter(tags=["Users"])


@user_router.put("/{user_id}", response_model=UserResponse)
def edit_user(user_id: UUID, request: UserUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing user's profile.
    """
    return update_user(str(user_id), request, db)


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a user's details by their ID.
    """
    return get_user_by_id(str(user_id), db)


@user_router.get("/username/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a user's details by their username, including password_hash.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return {
        "user_id": str(user.user_id),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "address": user.address,
        "phone_number": user.phone_number,
        "social_links": user.social_links,
        "password_hash": user.password_hash,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
