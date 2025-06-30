from fastapi import FastAPI
from app.models import Base
from database import engine

app = FastAPI()