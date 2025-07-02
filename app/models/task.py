from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship
from app.database.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    due_date = Column(DateTime, server_default=text("(CURRENT_TIMESTAMP + interval '3 days')"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")