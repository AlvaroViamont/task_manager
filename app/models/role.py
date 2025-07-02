from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("User", secondary="user_roles", back_populates="roles")