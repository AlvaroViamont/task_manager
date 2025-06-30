from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(..., description="Postgres host")
    POSTGRES_PORT: str = Field(..., description="Postgres port")
    TODO_DB: str = Field(..., description="Postgres DB")
    TODO_USER: str = Field(..., description="Postgres user")
    TODO_PASSWORD: str = Field(..., description="Postgres password")

    JWT_SECRET: str = Field(..., description="JWT Secret key")
    ALGORITHM: str = Field(..., description="JWT algorithm")

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.TODO_USER}:"
            f"{self.TODO_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.TODO_DB}"
        )

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore
