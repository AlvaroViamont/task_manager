from sqlalchemy import Column, Integer, String, Sequence, DateTime, text, ForeignKey, Table
from sqlalchemy.orm import Session, relationship
from fastapi import HTTPException
from database import Base

task_id_seq= Sequence('task_id_seq', start=1000) # type: ignore
role_id_seq= Sequence('role_id_seq', start=1) # type: ignore
user_id_seq= Sequence('user_id_seq', start=1) # type: ignore

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, task_id_seq, primary_key=True, server_default=task_id_seq.next_value())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    due_date = Column(DateTime, server_default=text("(CURRENT_TIMESTAMP + interval '3 days')"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")
    
    @classmethod
    def get_or_404(cls, db: Session, task_id: int):
        task = db.query(cls).filter(cls.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail=f"Tarea con id {task_id} no encontrada")
        return task

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, role_id_seq, primary_key=True, server_default=role_id_seq.next_value())
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
    @classmethod
    def get_or_404(cls, db: Session, task_id: int):
        task = db.query(cls).filter(cls.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail=f"Tarea con id {task_id} no encontrada")
        return task


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, user_id_seq, primary_key=True, server_default=user_id_seq.next_value())
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    @classmethod
    def get_or_404(cls, db: Session, task_id: int):
        task = db.query(cls).filter(cls.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail=f"Tarea con id {task_id} no encontrada")
        return task