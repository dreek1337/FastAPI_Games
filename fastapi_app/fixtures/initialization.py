from tortoise import Tortoise
from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    """
    Валидация .env для подключения к базе данных
    """
    password: str = Field(..., env='DATABASE_PASSWORD')
    user: str = Field(..., env='DATABASE_USER')
    database: str = Field(..., env='DATABASE_DB')
    host: str = Field(..., env='DATABASE_HOST')
    port: int = Field(5432, env='DATABASE_PORT')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_connection(self):
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


async def init() -> None:
    """
    Подключение к бд
    """
    await Tortoise.init(
        db_url=DatabaseSettings().db_connection,
        modules={'models': [
            "fill_models"
        ]}
    )
