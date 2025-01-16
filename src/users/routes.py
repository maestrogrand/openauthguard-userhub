from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.users.schemas import UserCreate, UserUpdate, UserResponse
from src.users.services import create_user, update_user, get_user_by_id
from src.users.models import User

router = APIRouter(tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new individual user.
    """
    return create_user(request, db)

@router.put("/edit/{user_id}", response_model=UserResponse)
def edit_user(user_id: str, request: UserUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing user's profile.
    """
    return update_user(user_id, request, db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a user's details by their ID.
    """
    return get_user_by_id(user_id, db)

@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a user's details by their username.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
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

@router.get("/tenant/{company_name}")
def get_tenant_by_company_name(company_name: str, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve tenant details by company name.
    """
    tenant = db.query(Tenant).filter(Tenant.company_name.ilike(company_name)).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found.")
    return {
        "tenant_id": tenant.tenant_id,
        "company_name": tenant.company_name,
        "created_at": tenant.created_at,
    }
