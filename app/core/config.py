from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    TODO_DB: str
    TODO_USER: str
    TODO_PASSWORD: str
    JWT_SECRET: str
    ALGORITHM: str = "HS256"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.TODO_USER}:{self.TODO_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.TODO_DB}"
        )

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore