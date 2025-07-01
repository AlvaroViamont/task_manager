from sqlalchemy import Column, Integer, String, Sequence, DateTime, text
from sqlalchemy.orm import declarative_base, Session
from fastapi import HTTPException

Base = declarative_base()

task_id_seq= Sequence('task_id_seq', start=1000) # type: ignore

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, task_id_seq, primary_key=True, server_default=task_id_seq.next_value())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    due_date = Column(DateTime, server_default=text("(CURRENT_TIMESTAMP + interval '3 days')"), nullable=False)
    
    @classmethod
    def get_or_404(cls, db: Session, task_id: int):
        task = db.query(cls).filter(cls.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail=f"Tarea con id {task_id} no encontrada")
        return task