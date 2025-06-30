from pydantic import BaseModel, Field, FutureDatetime
from typing import Optional

class TaskCore(BaseModel):
    title: str = Field(..., min_length=5, max_length=60, description="Task Title")
    descrisption: Optional[str] = Field(None, description="Task description")
    status: str = Field('pending', description="Task Status")
    due_date: FutureDatetime = Field(..., description="Task Status")

class TaskCreate (TaskCore):
    pass

class TaskUpdate (BaseModel):
    title: Optional[str] = Field(..., min_length=5, max_length=60, description="Task Title")
    descrisption: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field('pending', description="Task Status")
    due_date: Optional[FutureDatetime] = Field(..., description="Task Status")

class TaskResponse(TaskCore):
    task_id: int = Field(..., ge=0, description="Task ID")
    
    class Config:
        orm_mode = True