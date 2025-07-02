from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from role.schemas import RoleCreate, RoleResponse, RoleUpdate, RoleListResponse, RoleUpdateUsers, RoleRemoveUsers
from typing import Optional
from database import get_db
from models import Role, User

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/", response_model=RoleListResponse)
def get_all_roles(
    sort_by: Optional[str] = Query(None, description="Field to sort by (e.g., 'name')"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Order: asc or desc"),
    db: Session = Depends(get_db)
):
    valid_fields = {
        "id": Role.id,
        "name": Role.name,
    }
    query = db.query(Role)
    if sort_by:
        if sort_by not in valid_fields:
            raise HTTPException(status_code=400, detail=f"Invalid field for sorting: {sort_by}")
        ordering = asc(valid_fields[sort_by]) if order == "asc" else desc(valid_fields[sort_by])
        query = query.order_by(ordering)
    roles = query.all()
    return RoleListResponse(roles=roles)

@router.get("/{id}", response_model=RoleResponse)
def get_role_by_id(id: int, db: Session = Depends(get_db)):
    role = Role.get_or_404(db, id)
    return role

@router.put("/{id}", response_model=RoleResponse)
def update_role(id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    role = Role.get_or_404(db, id)
    update_data = role_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role, key, value)
    db.commit()
    db.refresh(role) 
    return role

@router.delete("/{id}", response_model=RoleResponse)
def delete_role(id: int, db: Session = Depends(get_db)):
    role = Role.get_or_404(db, id)
    db.delete(role)
    db.commit()
    return role

@router.put("/{id}/users", response_model=RoleResponse)
def update_role_users(id: int, role_update_users: RoleUpdateUsers, db: Session = Depends(get_db)):
    role = Role.get_or_404(db, id)
    user_ids = role_update_users.user_ids
    if not user_ids:
        raise HTTPException(status_code=400, detail="User IDs list cannot be empty")
    
    # Clear existing users and add new ones
    role.users.clear()
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        role.users.append(user)
    
    db.commit()
    db.refresh(role)
    return role

@router.delete("/{id}/users", response_model=RoleResponse)
def remove_role_users(id: int, role_remove_users: RoleRemoveUsers, db: Session = Depends(get_db)):
    role = Role.get_or_404(db, id)
    user_ids = role_remove_users.user_ids
    if not user_ids:
        raise HTTPException(status_code=400, detail="User IDs list cannot be empty")
    
    # Remove specified users from the role
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        if user in role.users:
            role.users.remove(user)
    
    db.commit()
    db.refresh(role)
    return role