from pydantic import BaseModel, Field, FutureDatetime, ConfigDict
from typing import Optional, Literal

class TaskCore(BaseModel):
    title: str = Field(..., min_length=5, max_length=60, description="Task Title")
    description: Optional[str] = Field(None, description="Task description")
    status: str = Field('pending', description="Task Status")
    due_date: FutureDatetime = Field(..., description="Task Status")

class TaskCreate (TaskCore):
    pass

class TaskUpdate (BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=60, description="Task Title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field('pending', description="Task Status")
    due_date: Optional[FutureDatetime] = Field(None, description="Task Status")

class TaskResponse(TaskCore):
    id: int = Field(..., ge=0, description="Task ID")
    
    model_config = ConfigDict(from_attributes=True)

class TaskStatusUpdate(BaseModel):
    status: Literal['pending', 'in_progress', 'completed'] = Field(..., description="Nuevo estado de la tarea")