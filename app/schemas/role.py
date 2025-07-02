from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List

class RoleCore(BaseModel):
    name: str = Field(..., description="Role's name")

class RoleCreate(RoleCore):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Role's name")

class RoleResponse(RoleCore):
    id: int = Field(..., ge=0, description="Role ID")
    
    model_config = ConfigDict(from_attributes=True)

class RoleInDB(RoleResponse):
    pass

class RoleListResponse(BaseModel):
    roles: List[RoleResponse] = Field(..., description="List of roles")
    model_config = ConfigDict(from_attributes=True)

class RoleUpdateUsers(BaseModel):
    user_ids: List[int] = Field(..., description="List of user IDs to be assigned to the role")

    model_config = ConfigDict(from_attributes=True)

class RoleRemoveUsers(BaseModel):
    user_ids: List[int] = Field(..., description="List of user IDs to be removed from the role")

    model_config = ConfigDict(from_attributes=True)

