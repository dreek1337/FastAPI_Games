from pydantic import BaseSettings, Field


class DataSettings(BaseSettings):
    """
    Валидация .env для подключения к базе данных
    """
    db_password: str = Field(..., env='DATABASE_PASSWORD')
    db_user: str = Field(..., env='DATABASE_USER')
    db_name: str = Field(..., env='DATABASE_DB')
    db_host: str = Field(..., env='DATABASE_HOST')
    db_port: int = Field(5432, env='DATABASE_PORT')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_connection(self):
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class AppDescription(BaseSettings):
    version: float = Field(..., env='FGAMES_VERSION')
    title: str = Field(..., env='FGAMES_TITLE')
    description: str = Field('Лучший в мире проект.')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
