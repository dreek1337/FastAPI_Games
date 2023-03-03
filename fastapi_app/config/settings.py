from pydantic import BaseModel, BaseSettings, Field


class PydanticSettings(BaseSettings):
    """
    Настройки для BaseSettings
    """
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DataSettings(PydanticSettings):
    """
    Валидация .env для подключения к базе данных
    """
    db_password: str = Field(..., env='DATABASE_PASSWORD')
    db_user: str = Field(..., env='DATABASE_USER')
    db_name: str = Field(..., env='DATABASE_DB')
    db_host: str = Field(..., env='DATABASE_HOST')
    db_port: int = Field(5432, env='DATABASE_PORT')

    @property
    def db_connection(self):
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class SiteSettings(PydanticSettings):
    """
    Настройки для ювикорна
    """
    host: str = Field(..., env="SITE_HOST")
    port: int = Field(..., env="SITE_PORT")
    loop: str = Field("asyncio")
    log_level: str = Field("info", env="SITE_LOG_LEVEL")
    reload_delay: float = Field(0.25, env="SITE_RELOAD_DELAY")


class AppDescription(PydanticSettings):
    """
    Описание приложения
    """
    version: float = Field(..., env='FGAMES_VERSION')
    title: str = Field(..., env='FGAMES_TITLE')
    description: str = Field('Лучший в мире проект.')


class TortoiseSettings(PydanticSettings):
    """
    Настройки орм
    """
    generate_schemas: bool = Field(True, env="TORTOISE_GENERATE_SCHEMAS")
    add_exception_handlers: bool = Field(True, env="DATABASE_EXCEPTION_HANDLERS")


class DataBaseModels(BaseModel):
    """
    Пути к моделям и миграциям
    """
    models: list[str] = Field(
        [
            "aerich.models",
            "database.models"
        ]
    )
    default_connection: str = Field("default")


class DataBaseSettings(BaseModel):
    """
    Объединение настроек для переменной TORTOISE_ORM
    """
    connections: dict = Field(default={"default": DataSettings().db_connection})
    apps: dict = Field(default={"models": DataBaseModels().dict()})
