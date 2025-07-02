from fastapi import FastAPI
from task.routes import router as task_router
from role.routes import router as role_router
from user.routes import router as user_router
from database import Base, engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔄 Esto se ejecuta al iniciar
    Base.metadata.create_all(bind=engine)
    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(role_router)
app.include_router(user_router)
app.include_router(task_router)


