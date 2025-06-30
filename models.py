from sqlalchemy import Column, Integer, String, Sequence, DateTime, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

task_id_seq= Sequence('task_id_seq', start=1000) # type: ignore

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, task_id_seq, primary_key=True, server_default=task_id_seq.next_value())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    due_date = Column(DateTime, server_default=text("(CURRENT_TIMESTAMP + interval '3 days')"), nullable=False)