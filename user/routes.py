from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from user.schemas import UserCreate, UserResponse, UserUpdate, UserListResponse, UserUpdateRoles, UserRemoveRoles
from typing import Optional
from database import get_db
from models import User, Role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.user_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(
        username=user.user_name,
        email=user.email,
        password=user.password,  # In a real application, hash the password
        full_name=user.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=UserListResponse)
def get_all_users(
    sort_by: Optional[str] = Query(None, description="Field to sort by (e.g., 'username', 'email')"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Order: asc or desc"),
    db: Session = Depends(get_db)
):
    valid_fields = {
        "id": User.id,
        "username": User.username,
        "email": User.email,
        "full_name": User.full_name,
    }
    query = db.query(User)
    if sort_by:
        if sort_by not in valid_fields:
            raise HTTPException(status_code=400, detail=f"Invalid field for sorting: {sort_by}")
        ordering = asc(valid_fields[sort_by]) if order == "asc" else desc(valid_fields[sort_by])
        query = query.order_by(ordering)
    users = query.all()
    return UserListResponse(users=users)

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user

@router.put("/{id}", response_model=UserResponse)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.put("/{id}/roles", response_model=UserResponse)
def update_user_roles(id: int, user_update_roles: UserUpdateRoles, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    role_ids = user_update_roles.role_ids
    if not role_ids:
        raise HTTPException(status_code=400, detail="Role IDs list cannot be empty")
    
    # Clear existing roles and add new ones
    user.roles.clear()
    for role_id in role_ids:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail=f"Role with id {role_id} not found")
        user.roles.append(role)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}/roles", response_model=UserResponse)
def remove_user_roles(id: int, user_remove_roles: UserRemoveRoles, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    role_ids = user_remove_roles.role_ids
    if not role_ids:
        raise HTTPException(status_code=400, detail="Role IDs list cannot be empty")
    
    # Remove specified roles
    for role_id in role_ids:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail=f"Role with id {role_id} not found")
        user.roles.remove(role)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    db.delete(user)
    db.commit()
    return

