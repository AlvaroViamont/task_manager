from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.schemas import TaskCreate, TaskResponse, TaskUpdate, TaskStatusUpdate
from typing import Optional, List
from app.database import get_db
from app.models import Task


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    status: Optional[str] = Query(None, description="Filtrar por estado de la tarea (ej: 'pending', 'in_progres', 'completed')"),
    sort_by: Optional[str] = Query(None, description="Campo por el cual ordenar (ej: 'status', 'due_date')"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Orden: asc o desc"),
    db: Session = Depends(get_db)
):
    valid_fields = {
        "id": Task.id,
        "title": Task.title,
        "status": Task.status,
        "due_date": Task.due_date,
    }
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if sort_by:
        if sort_by not in valid_fields:
            raise HTTPException(status_code=400, detail=f"Campo inválido para ordenamiento: {sort_by}")
        ordering = asc(valid_fields[sort_by]) if order == "asc" else desc(valid_fields[sort_by])
        query = query.order_by(ordering)
    tasks = query.all()
    return tasks

@router.get("/{id}", response_model=TaskResponse)
def get_task_by_id(id: int, db: Session = Depends(get_db)):
    task = Task.get_or_404(db, id)
    return task

@router.patch("/{id}", response_model=TaskResponse)
def update_task(id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = Task.get_or_404(db, id)
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task) 
    return task

@router.patch("/{id}", response_model=TaskResponse)
def change_task_status(id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    task = Task.get_or_404(db, id)
    task.status = status_update.status
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = Task.get_or_404(db, id)
    db.delete(task)
    db.commit()
    return