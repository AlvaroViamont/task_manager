from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional

class UserCore(BaseModel):
    user_name: str = Field(..., min_length=5, max_length=50, description="Users's name")
    email: EmailStr = Field(..., description="Users's mail")

class UserCreate(UserCore):
    password: str = Field(..., description="Users's passwords")
    full_name: Optional[str] = Field(None, description="Users's full name")
    role: int = Field(default=1, description="User role")

class UserUpdate(BaseModel):
    user_name: Optional[str] = Field(None, min_length=5, max_length=50, description="Users's name")
    email: Optional[EmailStr] = Field(None, description="Users's mail")
    full_name: Optional[str] = Field(None, description="Users's full name")

class UserUpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=5, max_length=20, description="Current password")
    new_password: str = Field(..., min_length=5, max_length=20, description="New password")
    confirm_new_password: str = Field(..., min_length=5, max_length=20, description="Confirm new password")

class UserLogin(BaseModel):
    user_name: str = Field(..., min_length=5, max_length=20, description="Username")
    password: str = Field(..., min_length=5, max_length=20, description="User password")

class UserResponse(UserCore):
    id: int = Field(..., ge=0, description="User ID")
    full_name: Optional[str] = Field(None, description="Users's full name")
    role: int = Field(default=1, description="User role")
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserResponse):
    hashed_password: str

class UserListResponse(BaseModel):
    users: list[UserResponse] = Field(..., description="List of users")
    model_config = ConfigDict(from_attributes=True)

class UserUpdateRoles(BaseModel):
    role_ids: list[int] = Field(..., description="List of role IDs to be assigned to the user")

    model_config = ConfigDict(from_attributes=True)

class UserRemoveRoles(BaseModel):
    role_ids: list[int] = Field(..., description="List of role IDs to be removed from the user")

    model_config = ConfigDict(from_attributes=True)